import csv
import json
import logging
import os

from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView, UpdateView

from pharma_track.models import Drug, Study
from website import settings
from website.local_settings import STATIC_ROOT, STATIC_URL

logger = logging.getLogger(__name__)


class ContactView(TemplateView):
    template_name = 'website/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_email'] = settings.CONTACT_EMAIL
        return context


class UserProfileView(SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'website/userprofile.html'
    fields = ['username', 'first_name', 'last_name', 'email']
    success_message = 'Userprofile saved'

    def get_context_data(self, **kwargs):
        if not self.request.user == self.get_object():
            raise PermissionDenied
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        if self.request.user != form.instance:
            raise PermissionDenied
        email = form.cleaned_data['email']
        users = User.objects.exclude(id=self.request.user.id).filter(email=email)
        if users.exists():
            form.add_error('email', 'Email is already used by another user.')
            logger.info('email is already used by another user')
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return '/userprofile/' + str(self.request.user.id) + '/'


class DrugSearchView(View):
    def post(self, request, *args, **kwargs):
        drug = self.request.POST.get('d', '')
        company = self.request.POST.get('c', '') or ''
        status = self.request.POST.get('s', '') or ''
        print("Search: {} - {} - {}".format(drug, company, status))
        result_objects = []
        if status:
            result_objects = Drug.objects.filter(
                Q(name__icontains=drug) | Q(sub_name__icontains=drug) | Q(indication__icontains=drug),
                company__icontains=company,
                studies__status__icontains=status).distinct()
        else:
            result_objects = Drug.objects.filter(
                Q(name__icontains=drug) | Q(sub_name__icontains=drug) | Q(indication__icontains=drug),
                company__icontains=company).distinct()
        context = {
            'models': result_objects
        }
        ret = {
            'drugs': render_to_string('website/_partials/_search_results.html', context),
        }
        return JsonResponse(ret)


class DrugExportView(View):
    def post(self, request, *args, **kwargs):
        drug = self.request.POST.get('d', '')
        company = self.request.POST.get('c', '') or ''
        status = self.request.POST.get('s', '') or ''
        print("Search: {} - {} - {}".format(drug, company, status))
        result_objects = []
        if status:
            result_objects = Drug.objects.filter(
                Q(name__icontains=drug) | Q(sub_name__icontains=drug) | Q(indication__icontains=drug),
                source__icontains=company,
                studies__status__icontains=status).distinct()
        else:
            result_objects = Drug.objects.filter(
                Q(name__icontains=drug) | Q(sub_name__icontains=drug) | Q(indication__icontains=drug),
                source__icontains=company).distinct()

        # Render response
        res = {
            'url': ''
        }
        file_name = "pharmatrack_drugs_Drug:{}_Company:{}_Status:{}_{}.csv".format(
            drug or 'All',
            company or 'All',
            status or 'All',
            timezone.now().isoformat()
        )
        path = os.path.join(STATIC_ROOT, file_name)
        print(path)
        try:
            with open(os.path.join(STATIC_ROOT, file_name), 'w+') as ifile:
                headers = [
                    'Company',
                    'Name',
                    'Other name',
                    'Potential Indication',
                    'Phase',
                    'NCT Number',
                    'Status',
                    'URL'
                ]

                writer = csv.writer(ifile)
                writer.writerow(headers)

                for drug in result_objects:
                    if drug.studies.all().count() == 0:
                        tdata = [
                            drug.source,
                            drug.name,
                            drug.sub_name or '-',
                            drug.indication or '-',
                            drug.phase,
                            '-',
                            '-',
                            '-'
                        ]
                        writer.writerow(tdata)

                    for study in drug.studies.all():
                        data = [
                            drug.source,
                            drug.name,
                            drug.sub_name or '-',
                            drug.indication or '-',
                            drug.phase,
                            study.nct_id,
                            study.status,
                            study.url
                        ]
                        writer.writerow(data)
        except Exception as e:
            print(e)
        else:
            res.update({
                'url': os.path.join(STATIC_URL, file_name)
            })
        return JsonResponse(res)


def drug_autocomplete(request):
    print(request)
    if request.is_ajax():
        query = request.GET.get("term", "")
        drugs = []
        drug_name = Drug.objects.filter(name__icontains=query).values_list(
                'name', flat=True).distinct()[:20]
        drugs.extend(list(drug_name))

        drug_sub_name = Drug.objects.filter(sub_name__icontains=query).values_list(
            'sub_name', flat=True).distinct()[:20]
        drugs.extend(list(drug_sub_name))

        drug_indication = Drug.objects.filter(indication__icontains=query).values_list(
            'indication', flat=True).distinct()[:20]
        drugs.extend(list(drug_indication))

        drugs = sorted(list(set(drugs)))[:20]

        data = json.dumps(list(drugs))
    mimetype = "application/json"
    return HttpResponse(data, mimetype)


def company_autocomplete(request):
    print(request)
    if request.is_ajax():
        query = request.GET.get("term", "")
        companies = Drug.objects.filter(source__icontains=query).values_list('source', flat=True).distinct()[:20]
        data = json.dumps(list(companies))
    mimetype = "application/json"
    return HttpResponse(data, mimetype)


def status_autocomplete(request):
    print(request)
    if request.is_ajax():
        query = request.GET.get("term", "")
        status = Study.objects.filter(status__icontains=query).values_list('status', flat=True).distinct()[:20]
        data = json.dumps(list(status))
    mimetype = "application/json"
    return HttpResponse(data, mimetype)

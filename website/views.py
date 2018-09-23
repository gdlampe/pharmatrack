import json
import logging

from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, UpdateView

from pharma_track.models import Drug, Study
from website import settings

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
        if drug and status:
            result_objects = Drug.objects.filter(
                name__icontains=drug,
                company__icontains=company,
                studies__status__icontains=status).distinct()
        elif drug:
            result_objects = Drug.objects.filter(
                name__icontains=drug,
                company__icontains=company).distinct()
        context = {
            'models': result_objects
        }
        ret = {
            'drugs': render_to_string('website/_partials/_search_results.html', context),
        }
        return JsonResponse(ret)


def drug_autocomplete(request):
    print(request)
    if request.is_ajax():
        query = request.GET.get("term", "")
        drugs = Drug.objects.filter(name__icontains=query).values_list('name', flat=True).distinct()[:20]
        data = json.dumps(list(drugs))
    mimetype = "application/json"
    return HttpResponse(data, mimetype)


def company_autocomplete(request):
    print(request)
    if request.is_ajax():
        query = request.GET.get("term", "")
        companies = Drug.objects.filter(company__icontains=query).values_list('company', flat=True).distinct()[:20]
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

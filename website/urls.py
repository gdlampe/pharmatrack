from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from website.views import drug_autocomplete, company_autocomplete, status_autocomplete, DrugSearchView, DrugExportView

urlpatterns = [
    # Generic Survey URLs
    path('api/', include([
        path('drugs/', drug_autocomplete, name='drug-autocomplete'),
        path('companies/', company_autocomplete, name='company-autocomplete'),
        path('status/', status_autocomplete, name='status-autocomplete'),
        path('search/', DrugSearchView.as_view(), name='drug-search'),
        path('export/', DrugExportView.as_view(), name='drug-export')
    ])),
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='website/index.html'), name='homepage'),
]

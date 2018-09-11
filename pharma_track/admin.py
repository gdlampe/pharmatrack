from django.contrib import admin
from pharma_track.models import Drug


class DrugAdmin(admin.ModelAdmin):
    model = Drug
    list_display = (
        'name',
        'sub_name',
        'indication',
        'phase',
        'company',
        'version'
    )
    search_fields = (
        'name',
    )

admin.site.register(Drug, DrugAdmin)
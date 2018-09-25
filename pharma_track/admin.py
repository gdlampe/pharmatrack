from django.contrib import admin
from pharma_track.models import Drug, Study


class StudyInline(admin.TabularInline):
    model = Study
    extra = 0
    min_num = 0

class DrugAdmin(admin.ModelAdmin):
    model = Drug
    list_display = (
        'name',
        'sub_name',
        'indication',
        'phase',
        'company',
        'source',
        'version'
    )
    search_fields = (
        'name',
    )
    inlines = [StudyInline,]


class StudyAdmin(admin.ModelAdmin):
    model = Study

admin.site.register(Drug, DrugAdmin)
admin.site.register(Study, StudyAdmin)
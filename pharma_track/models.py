from django.db import models
from django.db.models import CASCADE
from django.utils.translation import ugettext_lazy as _

PHASE_1 = 'Phase 1'
PHASE_2 = 'Phase 2'
PHASE_3 = 'Phase 3'
PHASE_4 = 'Phase 4'
PHASE_CHOICES = (
    (PHASE_1, _('Phase 1')),
    (PHASE_2, _('Phase 2')),
    (PHASE_3, _('Phase 3')),
    (PHASE_4, _('Phase 4')),
)

class Drug(models.Model):
    name = models.CharField(max_length=400, null=True, blank=True)
    sub_name = models.CharField(max_length=400, null=True, blank=True)
    indication = models.CharField(max_length=400, null=True, blank=True)
    phase = models.CharField(max_length=400, choices=PHASE_CHOICES, default=PHASE_1)
    company = models.CharField(max_length=400, null=True, blank=True)
    source = models.CharField(max_length=400, null=True, blank=True)
    version = models.PositiveIntegerField(default=1)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u"Drug: {} - Indication: {}".format(self.name, self.indication)

    class Meta:
        verbose_name = _('Drug')
        verbose_name_plural = _('Drugs')
        unique_together = (("name", "sub_name", "indication"),)

class Study(models.Model):
    drug = models.ForeignKey(to="Drug", on_delete=CASCADE, related_name="studies")
    nct_id = models.CharField(max_length=400, verbose_name=_('NCT Number'))
    title = models.CharField(max_length=400, verbose_name=_('Title'))
    acronym = models.CharField(max_length=400, verbose_name=_('Acronym'))
    status = models.CharField(max_length=400, verbose_name=_('Status'))
    study_results = models.CharField(max_length=400, verbose_name=_('Study Results'))
    conditions = models.CharField(max_length=400, verbose_name=_('Conditions'))
    interventions = models.CharField(max_length=400, verbose_name=_('Interventions'))
    outcome_measures = models.CharField(max_length=400, verbose_name=_('Outcome Measures'))
    sponsor = models.CharField(max_length=400, verbose_name=_('Sponsor/Collaborators'))
    gender = models.CharField(max_length=400, verbose_name=_('Gender'))
    age = models.CharField(max_length=400, verbose_name=_('Age'))
    phase = models.CharField(max_length=400, verbose_name=_('Phase'))
    enrollment = models.CharField(max_length=400, verbose_name=_('Enrollment'))
    funded_by = models.CharField(max_length=400, verbose_name=_('Funded Bys'))
    study_type = models.CharField(max_length=400, verbose_name=_('Study Type'))
    study_design = models.CharField(max_length=400, verbose_name=_('Study Designs'))
    other_ids = models.CharField(max_length=400, verbose_name=_('Other IDs'))
    start_date = models.CharField(max_length=400, verbose_name=_('Start Date'))
    primary_completion_date = models.CharField(max_length=400, verbose_name=_('Primary Completion Date'))
    completion_date = models.CharField(max_length=400, verbose_name=_('Completion Date'))
    first_posted = models.CharField(max_length=400, verbose_name=_('First Posted'))
    results_first_posted = models.CharField(max_length=400, verbose_name=_('Results First Posted'))
    last_update_posted = models.CharField(max_length=400, verbose_name=_('Last Update Posted'))
    locations = models.CharField(max_length=400, verbose_name=_('Locations'))
    study_documents = models.CharField(max_length=400, verbose_name=_('Study Documents'))
    url = models.CharField(max_length=400, verbose_name=_('URL'))

    def __str__(self):
        return u"Drug: {} - NCT Number: {}".format(self.drug, self.nct_id)

    class Meta:
        verbose_name = _('Study')
        verbose_name_plural = _('Studies')

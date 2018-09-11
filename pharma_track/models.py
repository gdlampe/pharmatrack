from django.db import models
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
    version = models.PositiveIntegerField(default=1)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u"Drug: {} - Indication: {}".format(self.name, self.indication)

    class Meta:
        verbose_name = _('Drug')
        verbose_name_plural = _('Drugs')
        unique_together = (("name", "sub_name", "indication"),)

# -*- coding: utf-8 -*-
from django import template
register = template.Library()


# noinspection PyUnusedLocal
@register.simple_tag(takes_context=True)
def get_phase(context, phase):
    try:
        return int(phase.split()[1])
    except Exception as e:
        print(e)
        return 1
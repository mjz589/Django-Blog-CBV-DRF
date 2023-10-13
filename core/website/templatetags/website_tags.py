from django import template
from django.template.defaultfilters import stringfilter
from datetime import datetime

register = template.Library()


@register.filter
@stringfilter
def upto(delimiter=None):
    now = datetime.today()
    return now.split(delimiter)[0]


upto.is_safe = True


# YEARS OF EXPERIENCE
@register.inclusion_tag("indeex/sections/counter.html", name="exp")
def years_of_experience():
    year_2022 = datetime(2022, 9, 5, 18, 00)
    now = datetime.today()
    experience = now.year - year_2022.year
    return experience


# @register.inclusion_tag('website/widgets/latest-works.html', name='latest_works')
# def latest_works(arg=3):
#     projects = Project.objects.filter(publish_status= True).order_by('-published_date')[:arg]
#     return {'latest_works': projects }

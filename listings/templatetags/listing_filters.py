from django import template

register = template.Library()

@register.filter(name='filter_status')
def filter_status(ads, status):
    """
    Filters a list of ads by their status.
    """
    return [ad for ad in ads if ad.status == status]
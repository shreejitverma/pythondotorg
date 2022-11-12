from django import template

from pages.models import Page

register = template.Library()


@register.simple_tag
def get_newest_pep_pages(limit=5):
    """ Retrieve the most recently added PEPs """
    return Page.objects.filter(
        path__startswith='dev/peps/',
        is_published=True,
    ).order_by('-created')[:limit]

from django import template

from ..models import Membership

register = template.Library()


@register.filter(name='user_location')
def parse_location(user):
    """
    Returns a formatted string of user location data.
    Adds a comma if the city is present, adds a space is the region is present

    Returns empty if no location data is present
    """

    path = ''

    try:
        membership = user.membership
    except Membership.DoesNotExist:
        return ''

    if membership.city:
        path += f"{membership.city}"
    if membership.region:
        if membership.city:
            path += ", "
        path += f"{membership.region}"
    if membership.country:
        if membership.region:
            path += " "
        elif membership.city:
            path += ", "
        path += f"{membership.country}"

    return path

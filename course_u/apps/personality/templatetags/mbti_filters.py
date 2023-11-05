# from django import template

# register = template.Library()

# @register.filter
# def dict_lookup(d, key):
#     return d.get(key, None)


# from django import template

# register = template.Library()

# @register.filter(name='dictlookup')
# def dictlookup(dictionary, key):
#     if key in dictionary:
#         return dictionary[key]
#     else:
#         return None

# from django import template

# register = template.Library()

# @register.filter(name='mbti_data_property')
# def mbti_data_property(dictionary, key, property_name):
#     if key in dictionary and property_name in dictionary[key]:
#         return dictionary[key][property_name]
#     else:
#         return None

from django import template

register = template.Library()

@register.filter(name='mbti_data_property')
def mbti_data_property(dictionary, key, property_name):
    return dictionary.get(key, {}).get(property_name, '')

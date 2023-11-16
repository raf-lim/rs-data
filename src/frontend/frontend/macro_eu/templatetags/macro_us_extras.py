from django import template

register = template.Library()


def keyvalue(dictionary: dict, key: str):
    """Gets dictionary value by key"""
    return dictionary.get(key)


register.filter("keyvalue", keyvalue)

from django import template

register = template.Library()

@register.simple_tag
def update_variable(value, amount):
    """Permet de mettre à jour une variable existante dans le template"""
    return value

@register.simple_tag
def incrementer(value, amount=1):
    try:
        return int(value) + amount
    except (ValueError, TypeError):
        return value
    
@register.simple_tag
def return_to_zero(value):
    return 0
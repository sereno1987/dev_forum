from django import template

register = template.Library()

# to manipulate the fields
@register.filter
def field_type(bound_filed):
    return bound_filed.field.widget.__class__.__name__

@register.filter
def input_class(bound_filed):
    css_class=""
    if bound_filed.form.is_bound:
        if bound_filed.errors:
            css_class='is-invalid'
        elif field_type(bound_filed) != 'PasswordInput':
            css_class = 'is-valid'
    return 'form-control {}'.format(css_class)

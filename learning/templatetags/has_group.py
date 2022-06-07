from django import template

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    """Тег проверяющий пользователя на состоянии в какой-либо группе.
        Пример использования {% if request.user|has_group:'teachers' %}"""
    return user.groups.filter(name=group_name).exists()

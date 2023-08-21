from enum import Enum, unique
from django.utils.translation import gettext_lazy as _


class BaseEnum(Enum):
    def __str__(self):
        return self.name

    @property
    def descriptive_name(self):
        return self.name.replace('_', ' ').title()

    @classmethod
    def choices(cls):
        choices = list()
        for item in cls:
            choices.append((item.value, _(item.descriptive_name)))
        return tuple(choices)


@unique
class RolesEnum(BaseEnum):
    USER = 'user'
    ADVISOR = 'advisor'

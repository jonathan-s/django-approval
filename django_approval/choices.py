from django.utils.translation import gettext_lazy as _

from djchoices import DjangoChoices, ChoiceItem


class Action(DjangoChoices):
    new = ChoiceItem('new', _('New'))
    update = ChoiceItem('update', _('Update'))
    deleted = ChoiceItem('deleted', _('Deleted'))


class Status(DjangoChoices):
    approved = ChoiceItem('approved', _('Approved'))
    rejected = ChoiceItem('rejected', _('Rejected'))
    none = ChoiceItem('', _('No action taken'))

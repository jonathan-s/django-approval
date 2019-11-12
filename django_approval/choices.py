from django.utils.translation import gettext_lazy as _

from djchoices import DjangoChoices, ChoiceItem


class Action(DjangoChoices):
    create = ChoiceItem('create', _('Create'))
    update = ChoiceItem('update', _('Update'))
    delete = ChoiceItem('delete', _('Delete'))


class Status(DjangoChoices):
    approved = ChoiceItem('approved', _('Approved'))
    rejected = ChoiceItem('rejected', _('Rejected'))
    none = ChoiceItem('', _('No action taken'))

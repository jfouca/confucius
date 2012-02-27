from django.db import models


class ConfuciusModel(models.Model):
    """
    Base class for models which belong to confucius.
    Used mainly to avoid adding a Meta class with the
    right app_label for each model.
    """
    class Meta:
        abstract = True
        app_label = 'confucius'


<<<<<<< HEAD
from confucius.models.account import Address, Email, Language, ActivationKey
from confucius.models.conference import (Action, Alert, Conference, Domain, Event, Membership, MessageTemplate, Reminder, Role, ReviewerResponse)
from confucius.models.submission import (Paper)
=======
from confucius.models.account import *
from confucius.models.conference import *
from confucius.models.submission import *
>>>>>>> 224597fc16a07cccf814e23c274d91138de40a88
from confucius.models.review import *

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


from confucius.models.account import *
from confucius.models.conference import *
from confucius.models.submission import *

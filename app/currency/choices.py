from django.db import models


class RateCurrencyChoices(models.IntegerChoices):
    EUR = 1, 'Euro'
    USD = 2, 'Dollar'
    JPY = 3, 'Japanese yen'
    GBP = 4, 'British Pound Sterling'
    AUD = 5, 'Australian dollar'

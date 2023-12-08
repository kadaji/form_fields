import datetime, os, json

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.template import Context, Template
from django.core import validators
from django.core.validators import RegexValidator, validate_email

from cron_validator import CronValidator

numeric = RegexValidator(r'^[0-9+]', 'Only digit characters.')

def validate_security_question(data):
    # print(data)
    # if data[1] != data[2]:
    #     raise ValidationError('Answers to the question don\'t match.')

    # return data
    data = data.replace('\'', '\"')

    try:
        data = json.loads(data)
    except:
        raise ValidationError('Answers cannot contain special characters.')

    if data[1] != data[2]:
        raise ValidationError('Answers to the question don\'t match.')
    
    return json.dumps(data)

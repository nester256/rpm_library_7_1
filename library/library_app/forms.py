from django.forms import Form, ChoiceField
from . import config


class WeatherForm(Form):
    location = ChoiceField(
        label='location',
        choices=config.LOCATIONS_NAMES
    )

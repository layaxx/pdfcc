from django.forms import MultiValueField, IntegerField, MultiWidget
from django import forms


class RGBField(MultiValueField):
    def __init__(self, **kwargs):
        # Define one message for all fields.
        error_messages = {
            'incomplete': 'Enter a country calling code and a phone number.',
        }
        # Or define a different message for each field.
        fields = (
            IntegerField(
                error_messages={
                    'incomplete': 'Enter a valid value for red number.'},
                min_value=0,
                max_value=255,
            ),
            IntegerField(
                error_messages={
                    'incomplete': 'Enter a valid value for green number.'},
                min_value=0,
                max_value=255,
            ),
            IntegerField(
                error_messages={
                    'incomplete': 'Enter a valid value for blue number.'},
                min_value=0,
                max_value=255,
            ),
        )
        super().__init__(
            error_messages=error_messages, fields=fields,
            require_all_fields=True, **kwargs
        )

    def compress(self, l):
        return l[0]


class RGBWidget(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [forms.NumberInput(attrs={'style': 'width:4rem', 'onchange': 'updateColors()'}),
                   forms.NumberInput(attrs={'style': 'width:4rem', 'onchange': 'updateColors()'}), forms.NumberInput(attrs={'style': 'width:4rem', 'onchange': 'updateColors()'}), ]
        super(RGBWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split('-')
        else:
            return ['', '', '']


class RGBField(forms.fields.MultiValueField):
    widget = RGBWidget

    def __init__(self, *args, **kwargs):
        list_fields = [IntegerField(min_value=0, max_value=255),
                       IntegerField(min_value=0, max_value=255),
                       IntegerField(min_value=0, max_value=255), ]
        super(RGBField, self).__init__(list_fields, *args, **kwargs)

    def compress(self, values):
        values = map(str, values)
        return '-'.join(values)

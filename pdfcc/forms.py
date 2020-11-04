from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from .validators import validate_file_size
from .costumfields import RGBField


class MyForm(forms.Form):

    pdf = forms.FileField(label='PDF File (required)',
                          validators=[validate_file_size])

    c1_old = RGBField(
        label='first Color to be replace (required)', initial='72-70-70')
    c1_new = RGBField(
        label='Color to replace first Color (required)', initial='255-255-255')

    c2_old = RGBField(label='second Color to be replace',
                      required=False, initial='255-255-255')
    c2_new = RGBField(label='Color to replace second Color',
                      required=False, initial='0-0-0')

    prec = forms.IntegerField(
        label='How far off can colors be and still be replaced', initial='2', min_value=0, max_value=255)

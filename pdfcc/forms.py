from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from .validators import validate_file_size
from .costumfields import RGBField


class MyForm(forms.Form):

    pdf = forms.FileField(label='PDF File (required)',
                          validators=[validate_file_size])

    # monochrome = forms.BooleanField(
    #   initial=False, label='Convert entire document to Monochrome (after substituting colors)')
    c1_old = RGBField(
        label='first Color to be replace (required)', initial='72-70-70')
    c1_new = RGBField(
        label='Color to replace first Color (required)', initial='255-255-255')

    c2_old = RGBField(label='second Color to be replace',
                      required=False, initial='253-253-253')
    c2_new = RGBField(label='Color to replace second Color',
                      required=False, initial='0-0-0')

    c3_old = RGBField(label='third Color to be replace',
                      required=False, initial='237-242-247')
    c3_new = RGBField(label='Color to replace third Color',
                      required=False, initial='0-0-0')

    c4_old = RGBField(label='fourth Color to be replace',
                      required=False, initial='250-192-144')
    c4_new = RGBField(label='Color to replace fourth Color',
                      required=False, initial='0-0-0')

    c5_old = RGBField(label='fifth Color to be replace',
                      required=False, initial='255-255-255')
    c5_new = RGBField(label='Color to replace fifth Color',
                      required=False, initial='0-0-0')

    color_count = forms.IntegerField(
        widget=forms.HiddenInput(), initial=2, required=False)

    images = forms.ChoiceField(choices=[(0, 'No processing'), (1, 'Make grayscale')],
                               initial=0, label='How should images be processed', widget=forms.RadioSelect)

    prec = forms.IntegerField(
        label='How far off can colors be and still be replaced', initial='4', min_value=0, max_value=255)

from django.shortcuts import render
from django.http import HttpResponse
from .forms import MyForm

# Imaginary function to handle an uploaded file.
from .utility import handle_uploaded_file


def index(request):
    if request.method == 'POST':
        form = MyForm(request.POST, request.FILES)
        if form.is_valid():
            colors = {'c1_new': form.cleaned_data['c1_new'], 'c1_old': form.cleaned_data['c1_old'],
                      'c2_new': form.cleaned_data['c2_new'], 'c2_old': form.cleaned_data['c2_old']}
            result = handle_uploaded_file(
                request.FILES.get('pdf'), colors, form.cleaned_data['prec'])
            context = {'pdf_b64': result.get(
                'b64'), 'pdf_filename': result.get('filename')}
            return render(request, 'pdfcc/success.html', context)
    else:
        form = MyForm()
    return render(request, 'pdfcc/index.html', {'form': form})


def process(request):
    return HttpResponse("processing nothing")

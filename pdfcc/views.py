from django.shortcuts import render
from django.http import HttpResponse
from .forms import MyForm

# Imaginary function to handle an uploaded file.
from .utility import handle_uploaded_file


def index(request):
    if request.method == 'POST':
        form = MyForm(request.POST, request.FILES)
        if form.is_valid():
            color_count = int(form.cleaned_data['color_count'])
            colors = {'c1_new': form.cleaned_data['c1_new'], 'c1_old': form.cleaned_data['c1_old'],
                      'c2_new': form.cleaned_data['c2_new'], 'c2_old': form.cleaned_data['c2_old']}
            if color_count > 2:
                colors['c3_new'] = form.cleaned_data['c3_new']
                colors['c3_old'] = form.cleaned_data['c3_old']
                if color_count > 3:
                    colors['c4_new'] = form.cleaned_data['c4_new']
                    colors['c4_old'] = form.cleaned_data['c4_old']
                    if color_count > 4:
                        colors['c5_new'] = form.cleaned_data['c5_new']
                        colors['c5_old'] = form.cleaned_data['c5_old']
            result = handle_uploaded_file(
                request.FILES.get('pdf'), colors, form.cleaned_data['prec'], form.cleaned_data['images'])
            context = {'form': form, 'pdf_b64': result.get(
                'b64'), 'pdf_filename': result.get('filename'), 'color_count': color_count}
            print(color_count)
            return render(request, 'pdfcc/index.html', context)
    else:
        form = MyForm()
    return render(request, 'pdfcc/index.html', {'form': form, 'color_count': '2'})


def process(request):
    return HttpResponse("processing nothing")

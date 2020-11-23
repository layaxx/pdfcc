from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import MyForm, MyFormAnalyse

# Imaginary function to handle an uploaded file.
from .utility import handle_uploaded_file, new_analyse, newest_replace


def ajax(request):
    if request.method == 'POST':
        form = MyFormAnalyse(request.POST, request.FILES)
        if form.is_valid():
            if len(request.POST) <= 1:
                return JsonResponse({'error': False, 'message': 'Uploaded Successfully', 'analysis_result': new_analyse(request.FILES.get('pdf'))})
            else:
                try:
                    b64, number_of_colors = newest_replace(
                        request.POST, request.FILES.get('pdf'))
                    return JsonResponse({'error': False, 'message': 'Substituted Successfully', 'b64': b64, 'noc': number_of_colors})
                except BaseException as e:
                    return JsonResponse({'error': True, 'message': str(e)})

        else:
            return JsonResponse({'error': True, 'message': 'Form was not valid. Please make sure you submitted a PDF.', 'errors': form.errors})
    return render(request, 'pdfcc/ajax.html', {'form': MyFormAnalyse()})


def analyse(request):
    if request.method == 'POST':
        form = MyFormAnalyse(request.POST, request.FILES)
        if form.is_valid():
            result = new_analyse(request.FILES.get('pdf'))
            return render(request, 'pdfcc/analyse.html', {'res': result, 'file': request.FILES.get('pdf')})
        else:
            print(form.errors)
    else:
        form = MyFormAnalyse()
    return render(request, 'pdfcc/analyse.html', {'form': form})


def result(request):
    print(list(request.FILES))
    return HttpResponse("jo passt")


def index(request):
    if request.method == 'POST':
        form = MyForm(request.POST, request.FILES)
        if form.is_valid():
            color_count = int(form.cleaned_data['color_count'])
            colors = {'c1_new': form.cleaned_data['c1_new'], 'c1_old': form.cleaned_data['c1_old'],
                      'c2_new': form.cleaned_data['c2_new'], 'c2_old': form.cleaned_data['c2_old']}
            """
                If anyone sees the code below: I am sorry
            """
            if color_count > 2:
                colors['c3_new'] = form.cleaned_data['c3_new']
                colors['c3_old'] = form.cleaned_data['c3_old']
                if color_count > 3:
                    colors['c4_new'] = form.cleaned_data['c4_new']
                    colors['c4_old'] = form.cleaned_data['c4_old']
                    if color_count > 4:
                        colors['c5_new'] = form.cleaned_data['c5_new']
                        colors['c5_old'] = form.cleaned_data['c5_old']
                        if color_count > 5:
                            colors['c6_new'] = form.cleaned_data['c6_new']
                            colors['c6_old'] = form.cleaned_data['c6_old']
                            if color_count > 6:
                                colors['c7_new'] = form.cleaned_data['c7_new']
                                colors['c7_old'] = form.cleaned_data['c7_old']
            result = handle_uploaded_file(
                request.FILES.get('pdf'), colors, form.cleaned_data['prec'], form.cleaned_data['images'])
            context = {'form': form, 'pdf_b64': result.get(
                'b64'), 'pdf_filename': result.get('filename'), 'color_count': color_count}
            print(color_count)
            return render(request, 'pdfcc/index.html', context)
        else:
            print(form.errors)
    else:
        form = MyForm()
    return render(request, 'pdfcc/index.html', {'form': form, 'color_count': '2'})


def process(request):
    return HttpResponse("processing nothing")

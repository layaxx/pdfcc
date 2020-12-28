from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utility import new_analyse, newest_replace


@csrf_exempt
def analyse(request):
    if len(request.POST) <= 1:
        color_list = new_analyse(request.FILES.get('file'))
        if len(color_list) < 1:
            return JsonResponse({'error': True, 'message': 'No Colors found in PDF', 'analysis_result': color_list})
        else:
            return JsonResponse({'error': False, 'message': 'Uploaded Successfully', 'analysis_result': color_list})
    return JsonResponse({"error": True, 'message': 'invalid request'})


@csrf_exempt
def process(request):
    try:
        b64, number_of_colors = newest_replace(
            request.POST, request.FILES.get('file'))
        return JsonResponse({'error': False, 'message': 'Substituted Successfully', 'b64': b64, 'noc': number_of_colors})
    except BaseException as e:
        return JsonResponse({'error': True, 'message': str(e)})


def index(request):
    return render(request, 'pdfcc/index.html')

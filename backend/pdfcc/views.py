from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utility_analyze import analyse_colors
from .utility_process import process_request


@csrf_exempt
def analyse(request):
    '''
    View for analysing a given PDF and returning a list of the colors found in it, along with
    a list of the pages the color was found on
    '''
    if len(request.POST) <= 1:
        # call the utility.new_analyse function to extract the color information from the PDF
        color_list = analyse_colors(request.FILES.get('file'))
        if len(color_list) < 1:
            # if no colors are found in the PDF, return a response indicating the problem
            return JsonResponse({'error': True, 'message': 'No Colors found in PDF', 'analysis_result': color_list})
        else:
            # return the result
            return JsonResponse({'error': False, 'message': 'Uploaded Successfully', 'analysis_result': color_list})
    return JsonResponse({"error": True, 'message': 'invalid request'})


@csrf_exempt
def process(request):
    '''
    Takes a PDF file labeled 'file' in the FILES part of the request
    and one or more entries in the POST part of the request that consist of valid hex color codes
    for both identifier and value
    '''
    try:
        # try to handle input and return new PDF encoded as Base64 if no Exceptions occur
        b64 = process_request(
            request.POST, request.FILES.get('file'))
        return JsonResponse({'error': False, 'message': 'Substituted Successfully', 'b64': b64})
    except ValueError as e:
        # if an Exception is raised during handling of the input, return the error message
        # most likely cause for this is if no (valid) colors are provided for substitution
        return JsonResponse({'error': True, 'message': str(e)})


def index(request):
    '''
    Returns the static Frontend Files
    '''
    return render(request, 'pdfcc/index.html')

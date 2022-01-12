import pikepdf
import io
from base64 import b64encode
from .color import color


def is_valid_color(hexcode):
    '''
    takes string as input and returns Boolean
    returns True iff the provided input is a valid hex color code
    This function does not care wether input has # prefix or not
    '''
    hexcode = hexcode.lower()
    valid_characters = ['0', '1', '2', '3', '4', '5', '6',
                        '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    if len(hexcode) == 7 and hexcode[0] == '#':
        hexcode = hexcode[1:7]
    if len(hexcode) == 6:
        for char in hexcode:
            if not char in valid_characters:
                return False
        return True
    return False


def process_request(post_data, old_pdf):
    '''
    Takes the POST part of the request and a PDF as input
    POST part is expected to contain at least one valid entry, otherwise Expection is raised
    valid entries consist of a valid colorcodes for both identifier and value
    Returns a Base64 encoded PDF with colors substituted according to entries in POST data
    '''
    # Part 1: extract color data from POST data
    dict_of_valid_colors = {}
    for key in post_data:
        if is_valid_color(key) and is_valid_color(post_data[key]):
            dict_of_valid_colors[key.replace(
                '#', '')] = color(post_data[key])

    if len(dict_of_valid_colors) == 0:
        # raise Exception if no valid entries are found
        raise ValueError("No valid colors were provided")

    # Part 2: generate a new PDF
    new_pdf = replace_colors(dict_of_valid_colors, old_pdf)

    # Part 3: B64 encode the new PDF
    b64 = str(b64encode(new_pdf))[2:-1]
    return b64


def replace_colors(dict_of_colors, old_pdf):
    '''
    Takes a dict of colors to be replaced, with hex color code of old color as identifier and
    color object of new color as value as well as a PDF as input
    Returns the new PDF as bytes
    '''
    list_of_operators = [pikepdf.Operator('sc'), pikepdf.Operator(
        'SC'), pikepdf.Operator('rg'), pikepdf.Operator('RG')]

    with pikepdf.Pdf.open(old_pdf) as pdf:
        # iterate over every page in the PDF
        for pageindex in range(len(pdf.pages)):
            page = pdf.pages[pageindex]
            content_stream = pikepdf.parse_content_stream(page)
            for entry in content_stream:
                if entry[1] in list_of_operators:
                    color_old_hexcode = color(entry[0]).get_hex()
                    color_new = dict_of_colors.get(
                        color_old_hexcode, color(color_old_hexcode))
                    if not color_new.get_hex() == color_old_hexcode:
                        color_new_rgb_list = color_new.get_rgb_1()
                        entry[0][0] = color_new_rgb_list[0]
                        entry[0][1] = color_new_rgb_list[1]
                        entry[0][2] = color_new_rgb_list[2]

            content_stream_new = pikepdf.unparse_content_stream(content_stream)
            page.Contents = pdf.make_stream(content_stream_new)
        stream_output = io.BytesIO()
        pdf.save(stream_output)
    return bytes(stream_output.getvalue())

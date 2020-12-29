import pikepdf
from pikepdf import Pdf
from base64 import b64encode
import io
import itertools


def isValidColor(hexcode):
    '''
    takes string as input and returns Boolean
    returns True iff the provided input is a valid hex color code
    This function does not care wether input has # prefix
    '''
    hexcode = hexcode.lower()
    validChars = ['0', '1', '2', '3', '4', '5', '6',
                  '7', '8' '9', 'a', 'b', 'c', 'd', 'e', 'f']
    if len(hexcode) == 7:
        if hexcode[0] == '#':
            hexcode = hexcode[1:7]
    if len(hexcode) == 6:
        for char in hexcode:
            if not char in validChars:
                return False
        return True
    return False


def replace(post_data, old_pdf):
    '''
    Takes the POST part of the request and a PDF as input
    POST part is expected to contain at least one valid entry, otherwise Expection is raised
    valid entries consist of a valid colorcodes for both identifier and value
    Returns a Base64 encoded PDF with colors substituted according to entries in POST data
    '''
    # Part 1: extract color data from POST data
    dict_of_valid_colors = {}
    for key in post_data:
        if isValidColor(key) and isValidColor(post_data[key]):
            dict_of_valid_colors[key] = post_data[key]
    if len(dict_of_valid_colors) == 0:
        # raise Expetion if no valid entries are found
        raise BaseException("No valid colors were provided")

    # Part 2: generate a new PDF
    new_pdf = replace_colors_new(dict_of_valid_colors, old_pdf)

    # Part 3: B64 encode the new PDF
    b64 = str(b64encode(new_pdf))[2:-1]
    return b64, len(dict_of_valid_colors)


def replace_colors_new(dict_of_colors, old_pdf):
    '''
    Takes a dict of colors to be replaced, with hex color code of old color as identifier and
    hex color code of new color as value, and a PDF as input
    Returns the new PDF as bytes
    '''
    with Pdf.open(old_pdf) as pdf:
        # iterate over every page in the PDF
        for pageindex in range(len(pdf.pages)):
            page = pdf.pages[pageindex]
            content_stream = pikepdf.parse_content_stream(page)
            for entry in content_stream:
                if str(entry[1]).lower() == 'sc':
                    color_old_red = round(entry[0][0] * 255)
                    color_old_green = round(entry[0][1] * 255)
                    color_old_blue = round(entry[0][2] * 255)
                    color_old_hexcode = rgb_to_hex(
                        color_old_red, color_old_green, color_old_blue)
                    color_new_hexcode = dict_of_colors.get(
                        color_old_hexcode, color_old_hexcode)
                    if not color_new_hexcode == color_old_hexcode:
                        color_new_rgb_list = hex_to_rgb(color_new_hexcode)
                        entry[0][0] = color_new_rgb_list[0]
                        entry[0][1] = color_new_rgb_list[1]
                        entry[0][2] = color_new_rgb_list[2]
            content_stream_new = pikepdf.unparse_content_stream(content_stream)
            page.Contents = pdf.make_stream(content_stream_new)
        stream_output = io.BytesIO()
        pdf.save(stream_output)
    return bytes(stream_output.getvalue())


def rgb_to_hex(r, g, b):
    '''
    Takes three integers representing RGB values as input and converts them to hex code
    '''
    return '#%02x%02x%02x' % (int(r), int(g), int(b))


def hex_to_rgb(hexcode):
    '''
    Takes a string as input and tries to convert it to RGB values, represented as
    list of structure [R, G, B]
    returns [0,0,0] for inputs of length < 6 or length > 7
    '''
    if len(hexcode) == 7:
        r = int(hexcode[1:3], base=16)
        g = int(hexcode[3:5], base=16)
        b = int(hexcode[5:7], base=16)
        return [r/255, g/255, b/255]
    elif len(hexcode) == 6:
        r = int(hexcode[0:2], base=16)
        g = int(hexcode[2:4], base=16)
        b = int(hexcode[4:6], base=16)
        return [r/255, g/255, b/255]
    else:
        return [0, 0, 0]


def analyse(pdf_input):
    ''''
    Takes a PDF as input 
    Analyses the PDF and tracks each color and the pages it appers on
    Returns a list of lists. Those lists contain 2 entries, 
    the hex code of the color and the Pages it appears on as a human readable string
    '''

    def ranges(iterable):
        '''
        Copied from somewhere on StackOverflow
        Used to convert the list of individual pages to a list of Page ranges
        '''
        iterable = sorted(set(iterable))
        for _, group in itertools.groupby(enumerate(iterable), lambda t: t[1] - t[0]):
            group = list(group)
            yield group[0][1], group[-1][1]

    def beautifyPages(input):
        '''
        Takes a list of page numbers as input
        Returns a string with human readable version of page ranges
        '''
        if len(input) == 1:
            return f'Page {input[0]}'
        elif len(input) == 2:
            return f'Pages {input[0]}+{input[1]}'
        else:
            ranges_list = list(ranges(input))
            result = 'Pages '
            for entry in ranges_list:
                if entry[0] == entry[1]:
                    result += f'{entry[0]}, '
                elif entry[0] + 1 == entry[1]:
                    result += f'{entry[0]}, {entry[1]}, '
                else:
                    result += f'{entry[0]}-{entry[1]}, '
            return result[:-2]

    colors_dictionary = {}
    with Pdf.open(pdf_input) as pdf:
        for pagenumber in range(len(pdf.pages)):
            page = pdf.pages[pagenumber]
            stream = pikepdf.parse_content_stream(page)
            for stream_entry in stream:
                if str(stream_entry[1]).lower() == 'sc':
                    color_string = ''
                    for color_decimal in stream_entry[0]:
                        color_string += str('000' +
                                            str(round(color_decimal * 255)))[-3:]
                    if not color_string in colors_dictionary:
                        colors_dictionary[color_string] = {'color': color_string,
                                                           'count': 1, 'pages': [pagenumber + 1]}
                    else:
                        colors_dictionary[color_string]['count'] += 1
                        colors_dictionary[color_string]['pages'].append(
                            pagenumber + 1)

        result = []
        with open('t.txt', 'w') as f:
            colors_list = []
            for color_key in colors_dictionary:
                colors_dictionary[color_key]['pages'] = list(
                    set(colors_dictionary[color_key]['pages']))
                colors_list.append(colors_dictionary[color_key])

            colors_list.sort(key=lambda x: len(x['pages']), reverse=True)
            for entry in colors_list:
                print(entry, file=f)
                result.append([rgb_to_hex(str(entry['color'][:3]), str(
                    entry['color'][3:6]), str(entry['color'][6:])), str(beautifyPages(entry['pages']))])
        return result

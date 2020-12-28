import pikepdf
from pikepdf import Pdf
from base64 import b64encode
import io
import itertools


def isValidColor(hexcode):
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


def newest_replace(post_data, old_pdf):
    list_of_valid_colors = {}
    for key in post_data:
        if len(key) == 7 and key[0] == '#':
            if (len(post_data[key]) == 7 and post_data[key][0] == '#') or len(post_data[key]) == 6:
                print(key)
                list_of_valid_colors[key] = post_data[key]
    if len(list_of_valid_colors) == 0:
        raise BaseException("No valid colors were provided")
    new_pdf = replace_colors_new(list_of_valid_colors, old_pdf)
    b64 = str(b64encode(new_pdf))[2:-1]
    return b64, len(list_of_valid_colors)


def replace_colors_new(list_of_colors, old_pdf):
    with Pdf.open(old_pdf) as pdf:
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
                    color_new_hexcode = list_of_colors.get(
                        color_old_hexcode, color_old_hexcode)
                    if not color_new_hexcode == color_old_hexcode:
                        color_new_rgb_list = hex_to_rgb(color_new_hexcode)
                        print(color_new_hexcode, color_new_rgb_list)
                        entry[0][0] = color_new_rgb_list[0]
                        entry[0][1] = color_new_rgb_list[1]
                        entry[0][2] = color_new_rgb_list[2]
            content_stream_new = pikepdf.unparse_content_stream(content_stream)
            page.Contents = pdf.make_stream(content_stream_new)
        stream_output = io.BytesIO()
        pdf.save(stream_output)
    return bytes(stream_output.getvalue())


def get_download_link(file, filename_input):
    pdf_base64_string = str(b64encode(file))[2:-1]
    filename_input = filename_input[0:-4]
    filename = filename_input + '-printable.pdf'
    return {'b64': pdf_base64_string, 'filename': filename}


def ranges(iterable):
    iterable = sorted(set(iterable))
    for _, group in itertools.groupby(enumerate(iterable), lambda t: t[1] - t[0]):
        group = list(group)
        yield group[0][1], group[-1][1]


def rgb_to_hex(r, g, b):
    return '#%02x%02x%02x' % (int(r), int(g), int(b))


def hex_to_rgb(hexcode):
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


def new_analyse(pdf_input):
    def beautifyPages(input):
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

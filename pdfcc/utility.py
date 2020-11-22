import pikepdf
from pikepdf import Pdf, Name, PdfImage
from base64 import b64encode
import io
import zlib
from PIL import ImageOps
import itertools


def newest_replace(postData, old_pdf):
    colorData = {}
    for key in postData:
        if len(key) == 7 and key[0] == '#':
            if len(postData[key]) == 7 and postData[key][0] == '#':
                colorData[key] = postData[key]
    if len(colorData) == 0:
        raise BaseException("No valid colors were provided")
    new_pdf = b"replace_colors_new(colorData, old_pdf)"
    b64 = str(b64encode(new_pdf))[2:-1]
    return b64


def handle_uploaded_file(pdf, colors_input, prec, mode):
    new_pdf = replace_colors(pdf, colors_input, prec, int(mode))
    return get_download_link(new_pdf, pdf.name)


def get_download_link(file, filename_input):
    pdf_base64_string = str(b64encode(file))[2:-1]
    filename_input = filename_input[0:-4]
    filename = filename_input + '-printable.pdf'
    return {'b64': pdf_base64_string, 'filename': filename}


def replace_colors(pdf_input, colors_input, prec, mode):
    with Pdf.open(pdf_input) as pdf:
        for x in range(len(pdf.pages)):
            page = pdf.pages[x]
            stream = pikepdf.parse_content_stream(page)
            for entry in stream:
                if str(entry[1]).lower() == 'sc':
                    if close_enough(entry[0], colors_input.get('c1_old'), prec):
                        print(entry[0][0], entry[0][1], entry[0][2])
                        newcolor = colors_input.get('c1_new').split('-')
                        newcolor = [int(x) / 255 for x in newcolor]
                        entry[0][0] = newcolor[0]
                        entry[0][1] = newcolor[1]
                        entry[0][2] = newcolor[2]
                        print(entry[0][0], entry[0][1], entry[0][2])
                    elif close_enough(entry[0], colors_input.get('c2_old'), prec):
                        print(entry[0][0], entry[0][1], entry[0][2])
                        newcolor = colors_input.get('c2_new').split('-')
                        newcolor = [int(x) / 255 for x in newcolor]
                        entry[0][0] = newcolor[0]
                        entry[0][1] = newcolor[1]
                        entry[0][2] = newcolor[2]
                    else:
                        if not colors_input.get('c3_old') is None:
                            if close_enough(entry[0], colors_input.get('c3_old'), prec):
                                print(entry[0][0], entry[0][1], entry[0][2])
                                newcolor = colors_input.get(
                                    'c3_new').split('-')
                                newcolor = [int(x) / 255 for x in newcolor]
                                entry[0][0] = newcolor[0]
                                entry[0][1] = newcolor[1]
                                entry[0][2] = newcolor[2]
                            if not colors_input.get('c4_old') is None:
                                if close_enough(entry[0], colors_input.get('c4_old'), prec):
                                    print(entry[0][0], entry[0]
                                          [1], entry[0][2])
                                    newcolor = colors_input.get(
                                        'c4_new').split('-')
                                    newcolor = [int(x) / 255 for x in newcolor]
                                    entry[0][0] = newcolor[0]
                                    entry[0][1] = newcolor[1]
                                    entry[0][2] = newcolor[2]
                                if not colors_input.get('c5_old') is None:
                                    if close_enough(entry[0], colors_input.get('c5_old'), prec):
                                        print(entry[0][0], entry[0]
                                              [1], entry[0][2])
                                        newcolor = colors_input.get(
                                            'c5_new').split('-')
                                        newcolor = [
                                            int(x) / 255 for x in newcolor]
                                        entry[0][0] = newcolor[0]
                                        entry[0][1] = newcolor[1]
                                        entry[0][2] = newcolor[2]
                                    if not colors_input.get('c6_old') is None:
                                        if close_enough(entry[0], colors_input.get('c6_old'), prec):
                                            print(entry[0][0], entry[0]
                                                  [1], entry[0][2])
                                            newcolor = colors_input.get(
                                                'c6_new').split('-')
                                            newcolor = [
                                                int(x) / 255 for x in newcolor]
                                            entry[0][0] = newcolor[0]
                                            entry[0][1] = newcolor[1]
                                            entry[0][2] = newcolor[2]
                                        if not colors_input.get('c7_old') is None:
                                            if close_enough(entry[0], colors_input.get('c7_old'), prec):
                                                print(entry[0][0], entry[0]
                                                      [1], entry[0][2])
                                                newcolor = colors_input.get(
                                                    'c7_new').split('-')
                                                newcolor = [
                                                    int(x) / 255 for x in newcolor]
                                                entry[0][0] = newcolor[0]
                                                entry[0][1] = newcolor[1]
                                                entry[0][2] = newcolor[2]
                        print(entry[0][0])

            new_content_stream = pikepdf.unparse_content_stream(stream)
            page.Contents = pdf.make_stream(new_content_stream)

            if mode == 1:
                for rawimagecode in page.images:
                    rawimage = page.images[rawimagecode]
                    pdfimage = PdfImage(rawimage)
                    rawimage = pdfimage.obj
                    pillowimage = pdfimage.as_pil_image()
                    grayscale = pillowimage.convert('L')
                    rawimage.write(zlib.compress(grayscale.tobytes()),
                                   filter=Name("/FlateDecode"))
                    rawimage.ColorSpace = Name("/DeviceGray")

            if mode == 2:
                for rawimagecode in page.images:
                    rawimage = page.images[rawimagecode]
                    pdfimage = PdfImage(rawimage)
                    rawimage = pdfimage.obj
                    pillowimage = pdfimage.as_pil_image()
                    clrs = pillowimage.getcolors()
                    if not clrs is None:
                        if len(clrs) < 5:
                            pass
                    pillowimage_inverted = ImageOps.invert(pillowimage)
                    rawimage.write(zlib.compress(pillowimage_inverted.tobytes()),
                                   filter=Name("/FlateDecode"))

        stream = io.BytesIO()
        pdf.save(stream)
    return bytes(stream.getvalue())


def close_enough(entry, color_input, prec):
    color_input = color_input.split('-')
    r1 = int(color_input[0])
    g1 = int(color_input[1])
    b1 = int(color_input[2])
    r2 = int(entry[0] * 255)
    g2 = int(entry[1] * 255)
    b2 = int(entry[2] * 255)
    return abs(r1 - r2) < prec and abs(g1 - g2) < prec and abs(b1 - b2) < prec


def ranges(iterable):
    iterable = sorted(set(iterable))
    for _, group in itertools.groupby(enumerate(iterable), lambda t: t[1] - t[0]):
        group = list(group)
        yield group[0][1], group[-1][1]


def rgb_to_hex(r, g, b):
    return '#%02x%02x%02x' % (int(r), int(g), int(b))


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

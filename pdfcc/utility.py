from decimal import Decimal
import pikepdf
from pikepdf import Pdf, Page, Name, PdfImage
from base64 import b64encode
import io
import zlib
from PIL import Image, ImageOps


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


def new_analyse(pdf_input):
    def mf(x):
        return (int(x.split(' - ')[0]), int(x.split(' - ')[1]), int(x.split(' - ')[2]))

    all_colors = []
    with Pdf.open(pdf_input) as pdf:
        for x in range(len(pdf.pages)):
            page = pdf.pages[x]
            stream = pikepdf.parse_content_stream(page)
            for entry in stream:
                if str(entry[1]).lower() == 'sc':
                    string = ''
                    for x in entry[0]:
                        string += str(round(x * 255)) + " - "
                    all_colors.append(string[:-3])

        all_colors = list(set(all_colors))
        all_colors.sort(key=mf)
        res = []
        for entry in all_colors:
            res.append([str(entry.split(
                ' - ')[0]), str(entry.split(' - ')[1]),  str(entry.split(' - ')[2])])
        return res

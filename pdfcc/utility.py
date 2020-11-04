from decimal import Decimal
import pikepdf
from pikepdf import Pdf, Page
from base64 import b64encode
import io


def handle_uploaded_file(pdf, colors_input, prec):
    new_pdf = replace_colors(pdf, colors_input, prec)
    return get_download_link(new_pdf, pdf.name)


def get_download_link(file, filename_input):
    pdf_base64_string = str(b64encode(file))[2:-1]
    filename_input = filename_input[0:-4]
    filename = filename_input + '-printable.pdf'
    return {'b64': pdf_base64_string, 'filename': filename}


def replace_colors(pdf_input, colors_input, prec):
    with Pdf.open(pdf_input) as pdf:
        for x in range(len(pdf.pages)):
            print(x)
            page = pdf.pages[x]
            stream = pikepdf.parse_content_stream(page)
            for entry in stream:
                if str(entry[1]) == 'sc':
                    if close_enough(entry[0], colors_input.get('c1_old'), prec):
                        print(entry[0][0], entry[0][1], entry[0][2])
                        entry[0][0] = 1
                        entry[0][1] = 1
                        entry[0][2] = 1
                    elif close_enough(entry[0], colors_input.get('c2_old'), prec):
                        print(entry[0][0], entry[0][1], entry[0][2])
                        entry[0][0] = 0
                        entry[0][1] = 0
                        entry[0][2] = 0
                    else:
                        print(entry[0][0])

            new_content_stream = pikepdf.unparse_content_stream(stream)

            page.Contents = pdf.make_stream(new_content_stream)
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

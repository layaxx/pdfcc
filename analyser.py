from pikepdf import Pdf
import pikepdf

with Pdf.open('010-Foundations-gray-5.pdf') as pdf:
    with open('t.txt', 'w') as f:
        for x in range(len(pdf.pages)):
            page = pdf.pages[x]
            stream = pikepdf.parse_content_stream(page)
            for entry in stream:
                if str(entry[1]).lower() == 'sc':
                    for x in entry[0]:
                        x = x*255
                        print(x, file=f, end='', sep='')
                        print('', file=f,)

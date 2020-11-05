from pikepdf import Pdf
import pikepdf


def mf(x):
    return (int(x.split(' - ')[0]), int(x.split(' - ')[1]), int(x.split(' - ')[2]))


all_colors = []
with Pdf.open('010-Foundations-gray.pdf') as pdf:
    with open('t.txt', 'w') as f:
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

        for entry in all_colors:
            print(entry, file=f)
            # print('', file=f,)

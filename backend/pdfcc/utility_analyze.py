import itertools
import pikepdf
from .color import color


def ranges(iterable):
    '''
    Copied from somewhere on StackOverflow
    Used to convert the list of individual pages to a list of Page ranges
    '''
    iterable = sorted(set(iterable))
    for _, group in itertools.groupby(enumerate(iterable), lambda t: t[1] - t[0]):
        group = list(group)
        yield group[0][1], group[-1][1]


def human_readable_string_from_list_of_pages(input):
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


def analyse_colors(pdf_input):
    '''
    Takes a PDF as input
    Analyses the PDF and tracks each color and the pages it appers on
    Returns a list of tuples. Those tuples contain 2 entries,
    the hex code of the color and the Pages it appears on as a human readable string
    '''

    list_of_operators = [pikepdf.Operator('sc'), pikepdf.Operator(
        'SC'), pikepdf.Operator('rg'), pikepdf.Operator('RG')]
    # , pikepdf.Operator('rg'), pikepdf.Operator('RG')
    colors_dictionary = {}
    with pikepdf.Pdf.open(pdf_input) as pdf:
        # iterate over Pages in the PDF
        for pagenumber in range(len(pdf.pages)):
            page = pdf.pages[pagenumber]
            stream = pikepdf.parse_content_stream(page)
            filtered_stream = list(
                filter(lambda x: x[1] in list_of_operators, stream))

            unique_colors = list(
                set(['#' + color(x[0]).get_hex() for x in filtered_stream]))

            for colorcode in unique_colors:
                if colorcode in colors_dictionary:
                    colors_dictionary[colorcode].append(pagenumber + 1)
                else:
                    colors_dictionary[colorcode] = [pagenumber + 1]

        colors_list = [(k, v)
                       for k, v in colors_dictionary.items()]

        colors_list.sort(key=lambda x: len(x[1]), reverse=True)

        return [(k, human_readable_string_from_list_of_pages(v)) for k, v in colors_list]

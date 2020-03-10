from PIL import Image
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r'*****\Tesseract-OCR\tesseract.exe'

files = ['brezen.png', 'cerven.png', ]

"""
Scan_files projde obrazky z files a prevede je do textove podoby do slozky data
"""
def image_to_txt():
    for file in files:
        data = pytesseract.image_to_string(Image.open(r'*****\PythonForexFactoryDownloader\images_to_read\%s' % file))

        path = r'*****\PythonForexFactoryDownloader\images_to_read\data\%s.txt' % file
        with open(path, "w") as f:
            f.write(data)

"""
Parser pro prevod vygenerovanych txt souboru z metody scan_files. Prevede je do formatu, ktery nasledne muzu pouzit v MetaTrader 4 pro nakresleni car vsech urovni pomoci scriptu 'drawlines'
"""
def parse_txt_files():
    final_final_dates_string = '{'
    final_final_directions_string = '{'
    final_final_prices_string = '{'

    for file in files:
        path = r'******\PythonForexFactoryDownloader\images_to_read\data\%s.txt' % file
        result = []

        symbols = []
        dates = []
        directions = []
        prices = []

        # Toto neni uplne nejlepsi reseni, kazdopadne tesseract nedokazal presne rozlisit vsechny znaky
        with open(path, "r") as f:
            for line in f.readlines():
                if line == ' \n' or line == '\n':
                    pass
                else:
                    if 'Zisk' in line or 'Ztrata' in line:
                        line = line.replace('_', " ")

                        lines = line.split(' ')

                        testlist = [x for x in lines if not 'supp' in x]
                        testlist = [x for x in testlist if not '|' in x]
                        testlist = [x for x in testlist if not 'Zisk' in x]
                        testlist = [x for x in testlist if not 'Ztr' in x]
                        testlist = [x for x in testlist if not 'Inst.' in x]
                        testlist = [x for x in testlist if not 'inst' in x]
                        testlist = [x for x in testlist if not 'posti' in x]
                        testlist = [x for x in testlist if not 'St' in x]
                        testlist = [x for x in testlist if not 'rezi' in x]
                        testlist = [x for x in testlist if not 'nab' in x]
                        testlist = [x for x in testlist if not 'pop' in x]
                        testlist = [x for x in testlist if not 'op' in x]
                        testlist = [x for x in testlist if not 'bar' in x]
                        testlist = [x for x in testlist if not '\n' in x]

                        if '.' not in testlist[len(testlist) - 1]:
                            testlist = testlist[:len(testlist) - 1]

                        final_line = []

                        for l in testlist:
                            if '/' in l:
                                symbols.append(l.replace(',', '').replace('.', ''))
                                final_line.append(l.replace(',', '').replace('.', ''))
                            if 'Short' in l or 'Long' in l:
                                directions.append(l.replace(',', '').replace('.', ''))
                                final_line.append(l.replace(',', '').replace('.', ''))
                            regexp = re.compile(r'\d\d\.\d\d\.\d\d\d\d')
                            if regexp.search(l):
                                dates.append(l.replace(',', ''))
                                final_line.append(l.replace(',', ''))
                            regexp = re.compile(r'^\d{1}\.\d+')
                            regexp2 = re.compile(r'^\d{3}\.\d+')
                            if regexp.search(l) or regexp2.search(l) or '-' in l:
                                if '.' in l[len(l)-1]:
                                    l = l[:-1]
                                prices.append(l.replace(',', ''))
                                final_line.append(l.replace(',', ''))

                        result.append(final_line)

        if len(prices) == len(dates) == len(directions) == len(symbols):
            print("PASSED")
        else:
            print("FAIL at: %s" % result)

        selected_symbol = select_symbol(symbol='GBP/USD', array=result)

        final_dates_string = ''
        final_prices_string = ''
        final_directions_string = ''

        for item in selected_symbol:
            final_dates_string += 'D\'%s\', ' % item[0]
            final_prices_string += '"%s", ' % item[3]
            final_directions_string += '"%s", ' % item[2]

        final_final_dates_string += final_dates_string
        final_final_directions_string += final_directions_string
        final_final_prices_string += final_prices_string

    final_final_dates_string += '};'
    final_final_directions_string += '};'
    final_final_prices_string += '};'

    print(final_final_prices_string)
    print(final_final_dates_string)
    print(final_final_directions_string)

def select_symbol(symbol, array):
    return [x for x in array if symbol in x]


if __name__ == '__main__':
    image_to_txt()
    parse_txt_files()

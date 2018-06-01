import json
import os
import cv2
import pytesseract
import requests
from bs4 import BeautifulSoup
from halo import Halo

try:
    import Image
except ImportError:
    from PIL import Image


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_answer(question, optionA, optionB, optionC):
    spinner = Halo(text='Finding Answer for you ..', spinner='bouncingBar')
    spinner.start()

    r = requests.get("http://google.com/search?q=" + question)
    soup = BeautifulSoup(r.text, 'html.parser')
    response = soup.find_all("span", class_="st")
    res = str(r.text)

    countoption1 = res.count(optionA)
    countoption2 = res.count(optionB)
    countoption3 = res.count(optionC)
    s=1

    maxcount = max(countoption1, countoption2, countoption3)
    sumcount = countoption1 + countoption2 + countoption3
    sumcount=sumcount+0.1

    probA = round(((countoption1 / sumcount) * 100), 2)
    probB = round(((countoption2 / sumcount) * 100), 2)
    probC = round(((countoption3 / sumcount) * 100), 2)
    #   " }"+

    print("\n" + question +  "\n")
    if countoption1 == maxcount:
        print(bcolors.OKGREEN + "A{" + optionA + " }" + bcolors.ENDC + "  -: " + str(probA))
        print(bcolors.BOLD + "B{" + optionB + " }" + bcolors.ENDC + "  -: " + str(probB))
        print(bcolors.BOLD + "C{" + optionC + " }" + bcolors.ENDC + "  -: " + str(probC) + "\n")
    elif countoption2 == maxcount:
        print(bcolors.BOLD + "A{" + optionA + " }" + bcolors.ENDC + "  -: " + str(probA))
        print(bcolors.OKGREEN + "B{" + optionB + " }" + bcolors.ENDC + "  -: " + str(probB))
        print(bcolors.BOLD + "C{" + optionC + " }" + bcolors.ENDC + "  -: " + str(probC) + "\n")
    else:
        print(bcolors.BOLD + "A{" + optionA + " }" + bcolors.ENDC + "  -: " + str(probA))
        print(bcolors.BOLD + "B{" + optionB + " }" + bcolors.ENDC + "  -: " + str(probB))
        print(bcolors.OKGREEN + "C{" + optionC + " }" + bcolors.ENDC + "  -: " + str(probC) + "\n")

    spinner.succeed()
    spinner.stop()


def get_screen_shot(demo):
    if demo:
        screenfile = 'screendemo.png'
    else:
        os.system("adb exec-out screencap -p > screen.png")
        screenfile = 'screen.png'
    i = Image.open(screenfile)
    width, height = i.size
    frame = i.crop((0, 470, width, height - 200))
    filename = 'temp.png'
    frame.save(filename)

    spinner = Halo(text='Image reading', spinner='dots2')
    spinner.start()

    filename = cv2.imread(filename)
    gray = cv2.cvtColor(filename, cv2.COLOR_BGR2GRAY)
    # gray = cv2.threshold(gray, 5, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    filename2 = "screen{}.png".format(os.getpid())
    cv2.imwrite(filename2, gray)

    i = Image.open(filename2)

    frame = i.crop((0, 0, width, 150))
    frame.save('quest.png')

    frame = i.crop((120, 175, width - 120, 250))
    frame.save('A.png')

    frame = i.crop((120, 315, width - 120, 380))
    frame.save('B.png')

    frame = i.crop((120, 450, width - 120, 510))
    frame.save('C.png')

    question = pytesseract.image_to_string(Image.open('quest.png'))
    optionA = pytesseract.image_to_string(Image.open('A.png'))
    optionB = pytesseract.image_to_string(Image.open('B.png'))
    optionC = pytesseract.image_to_string(Image.open('C.png'))

    spinner.succeed()
    spinner.stop()
    get_answer(question,optionA,optionB,optionC)

    '''sample_questions = json.loads(open("questions.json").read())
    for key in sample_questions:
        options = sample_questions[key]
        print key
        get_answer(key, options[0], options[1], options[2])'''

    os.remove(filename2)
    os.remove('quest.png')
    os.remove('A.png')
    os.remove('B.png')
    os.remove('C.png')


# TODO: when you run against the demo mode set demo = True
demo = True
# TODO: when you run against the live game uncomment the following line
#demo = False
if __name__ == "__main__":
    while True:
        raw_input("When you see question press Enter")
        get_screen_shot(demo)

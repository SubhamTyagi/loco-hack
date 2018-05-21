"""

    TODO:
    * Attempt to google wiki \"...\" part of question
    * Rid of common appearances in 3 options
    * Automate screenshot process
    * Implement Asynchio for concurrency
    //Script is in working condition at all times with python27
    //TODO is for improving accuracy

"""

# Answering bot for LOCO
import json
import urllib2
from bs4 import BeautifulSoup
from google import google
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import sys

from halo import Halo


# for terminal colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# sample questions from previous games
sample_questions = {}

# list of words to clean from the question during google search
remove_words = []

# negative words
negative_words = []


# load sample questions
def load_json():
    global remove_words, sample_questions, negative_words
    remove_words = json.loads(open("libs/settings.json").read())["remove_words"]
    negative_words = json.loads(open("libs/settings.json").read())["negative_words"]
    sample_questions = json.loads(open("libs/questions.json").read())


# simplify question and remove which,what....etc //question is string
def simplify_ques(question):
    neg = False
    qwords = question.lower().split()
    if [i for i in qwords if i in negative_words]:
        neg = True
    cleanwords = [word for word in qwords if word.lower() not in remove_words]
    temp = ' '.join(cleanwords)
    clean_question = ""
    # remove ?
    for ch in temp:
        if ch != "?" or ch != "\"" or ch != "\'":
            clean_question = clean_question + ch

    return clean_question.lower(), neg


# get web page
def get_page(link):
    try:
        if link.find('mailto') != -1:
            return ''
        req = urllib2.Request(link, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})
        html = urllib2.urlopen(req).read()
        return html
    except (urllib2.URLError, urllib2.HTTPError, ValueError) as e:
        return ''


# split the string
def split_string(source):
    splitlist = ",!-.;/?@ #"
    output = []
    atsplit = True
    for char in source:
        if char in splitlist:
            atsplit = True
        else:
            if atsplit:
                output.append(char)
                atsplit = False
            else:
                output[-1] = output[-1] + char
    return output


# answer by combining two words
def smart_answer(content, qwords):
    zipped = zip(qwords, qwords[1:])
    points = 0
    for el in zipped:
        if content.count(el[0] + " " + el[1]) != 0:
            points += 1000
    return points


# use google to get wiki page
def google_wiki(sim_ques, options, neg):
    spinner = Halo(text='Googling. and searching Wikipedia', spinner='dots2')
    spinner.start()
    # number of google result pages
    num_pages = 1
    points = list()
    content = ""
    maxo = ""
    maxp = -sys.maxsize
    words = split_string(sim_ques)
    for o in options:

        o = o.lower()
        original = o
        o += ' wiki'

        # get google search results for option + 'wiki'
        search_wiki = google.search(o, num_pages)

        link = search_wiki[0].link
        content = get_page(link)
        soup = BeautifulSoup(content, "lxml")
        page = soup.get_text().lower()

        temp = 0

        for word in words:
            temp = temp + page.count(word)
        temp += smart_answer(page, words)
        if neg:
            temp *= -1
        points.append(temp)
        if temp > maxp:
            maxp = temp
            maxo = original
    spinner.succeed()
    spinner.stop()
    return points, maxo


# take screenshot from phone and return text from that screenshot if it is not demo
def take_screenshot_and_get_text(demo):
    spinner = Halo(text='Reading screen', spinner='bouncingBar')
    spinner.start()

    if demo:
        screenshot_file = "screendemo.png"
    else:
        os.system("adb exec-out screencap -p > screen.png")
        screenshot_file = "screen.png"

    # save a croped image to temp.png file
    i = Image.open(screenshot_file)
    width, height = i.size
    frame = i.crop((0, 470, width, height - 200))

    filename = 'temp.png'
    frame.save(filename)

    # load the image
    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV| cv2.THRESH_OTSU)[1]

    # gray = cv2.medianBlur(gray, 2)
    # store grayscale image as a temp file to apply OCR

    filename2 = "screen{}.png".format(os.getpid())
    cv2.imwrite(filename2, gray)
    i = Image.open(filename2)

    frame = i.crop((0, 0, width, 150))
    frame.save('quest.png')

    frame = i.crop((120, 160, width - 120, 240))
    frame.save('A.png')

    frame = i.crop((120, 300, width - 120, 370))
    frame.save('B.png')

    frame = i.crop((120, 430, width - 120, 510))
    frame.save('C.png')

    question = pytesseract.image_to_string(Image.open('quest.png'))
    option_A = pytesseract.image_to_string(Image.open('A.png'))
    option_B = pytesseract.image_to_string(Image.open('B.png'))
    option_C = pytesseract.image_to_string(Image.open('C.png'))

    options = list()
    options.append(option_A)
    options.append(option_B)
    options.append(option_C)


    '''os.remove(filename2)
    os.remove(filename)
    os.remove('quest.png')
    os.remove('A.png')
    os.remove('B.png')
    os.remove('C.png')'''
    # TODO: os.remove(screenshot_file)

    print('\n'+ question)
    print '1   ' + option_A
    print '2   ' + option_B
    print '3   ' + option_C

    spinner.succeed()
    spinner.stop()
    return question, options


# return points for sample_questions sample # QUESTION: are in libs/questions.json file
def get_points_sample():
    simq = ""
    x = 0
    for key in sample_questions:
        x = x + 1
        points = []
        simq, neg = simplify_ques(key)
        options = sample_questions[key]
        simq = simq.lower()
        maxo = ""
        points, maxo = google_wiki(simq, options, neg)
        print("\n" + str(x) + ". " + bcolors.UNDERLINE + key + bcolors.ENDC + "\n")
        for point, option in zip(points, options):
            if maxo == option.lower():
                option = bcolors.OKGREEN + option + bcolors.ENDC
            print(option + " { points: " + bcolors.BOLD + str(point) + bcolors.ENDC + " }\n")


# return points for live game // by screenshot
def get_points_live(demo):
    neg = False
    question, options = take_screenshot_and_get_text(demo)
    simq = ""
    points = []
    simq, neg = simplify_ques(question)
    maxo = ""
    m = 1
    if neg:
        m = -1
    points, maxo = google_wiki(simq, options, neg)
    print("\n" + bcolors.UNDERLINE + question + bcolors.ENDC + "\n")
    for point, option in zip(points, options):
        if maxo == option.lower():
            option = bcolors.OKGREEN + option + bcolors.ENDC
        print(option + " { points: " + bcolors.BOLD + str(point * m) + bcolors.ENDC + " }\n")


# menu// main func
if __name__ == "__main__":
    load_json()
    while (1):
        keypressed = raw_input(
            bcolors.WARNING + '\nPress s or Enter to screenshot live game, d to run against sample questions '
                              'or q to quit:\n' + bcolors.ENDC)
        if keypressed == 's':
            get_points_live(False)
        elif keypressed == 'd':
            get_points_live(True)
            # TODO: get_points_sample()
        elif keypressed == 'q':
            break
        else:
            get_points_live(False)
            print(bcolors.FAIL + "\nUnknown input" + bcolors.ENDC)

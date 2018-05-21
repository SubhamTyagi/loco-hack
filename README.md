# LOCO-HACK
![License: MIT][ico-license]



A bot to help answer questions on trivia apps like LOCO. This bot takes screenshot of the game from phone and uses googles tesseract OCR to read the questions and options. It automates the process of googling of the answers and gives the most likely answer! It is 85%+ accurate!

Since it is against the policy of LOCO i do not encourage anyone to use this during a live game and this is purely for educational purposes.  

## Packages Used

Use python 2.7  or you can use python37(some compatibility issues )particular the packages/libraries used are...

* JSON - Data Storage
* Pillow - Image manipulation
* Google-Search-API - Google searching
* pytesseract - Google's free/open source OCR (requires separate installation)
* beautifulsoup4 - Parse google searches/html
* lxml - Beautifulsoup parser
* opencv2 - Image manipulation
* pyscreenshot - Take screenshot of the game


*To easily install these*
1. Install python 2.7
2. Install above packages
    * `$ pip install -r requirements.txt`
3. For tesseract
    * `$ brew install tesseract`
4. For opencv
    * `$ brew install opencv`
5. Android adb
    * `Either you have android sdk or minimal ADB`

## Usage

Make sure all packages above are installed. For android phones use, To use this script :

```bash
$ git clone https://github.com/SubhamTyagi/loco-hack
$ cd loco-hack
$ pip install -r requirements.txt
$ python bot.py

Press l for live game, s to run against sample questions or q to quit:
s
...Question...
```

## Contributing

All contributions welcome.

## TODO: Improving speed

## Credits
- [SHUBHAM TYAGI][link-author]

- [All Contributors][link-contributors]

## Useful links

- [Wikipedia-API][link-wikiapi]
- [Google-Search-API][link-gapi]
- [Tesseract][link-tesseract]

## License

The MIT License (MIT)

[ico-license]: https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square

[link-author]: https://github.com/SubhamTyagi/

[link-contributors]: ../../contributors
[link-wikiapi]: https://pypi.python.org/pypi/wikipedia
[link-gapi]: https://github.com/abenassi/Google-Search-API
[link-mike]: https://github.com/mikealmond/hq-trivia-assistant
[link-tesseract]: https://github.com/tesseract-ocr/tesseract/wiki
[sampq]: ()

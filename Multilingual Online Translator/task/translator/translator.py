import requests
from bs4 import BeautifulSoup
import sys


def print_result(translate_dict, n_translate):
    for lang, tr_list in translate_dict.items():
        print(lang.capitalize(), "Translations:")
        for i, translate in enumerate(tr_list['translate']):
            if i < n_translate:
                print(translate)
        print()
        print(lang.capitalize(), "Examples:")
        for i, example in enumerate(tr_list['example']):
            if i < n_translate * 2:
                print(example)
                if i % 2 != 0:
                    print()


def save_to_file(translate_dict, n_translate, word):
    original_stdout = sys.stdout
    with open(word + '.txt', 'w+', encoding="utf-8") as f:
        sys.stdout = f
        print_result(translate_dict, n_translate)
        sys.stdout = original_stdout


n_translate = 1
translate_dict = {}
lang_from = None
lang_to = None
headers = {'User-Agent': 'Mozilla/5.0'}
lang_dict = {
    1: 'Arabic',
    2: 'German',
    3: 'English',
    4: 'Spanish',
    5: 'French',
    6: 'Hebrew',
    7: 'Japanese',
    8: 'Dutch',
    9: 'Polish',
    10: 'Portuguese',
    11: 'Romanian',
    12: 'Russian',
    13: 'Turkish'}
print("Hello, you're welcome to the translator. Translator supports:")
for key, value in lang_dict.items():
    print('{0}: {1}'.format(key, value))
while lang_from not in lang_dict.keys():
    lang_from = int(input('Type the number of your language:'))
while lang_to not in lang_dict.keys() and lang_to !=0:
    lang_to = int(input("Type the number of language you want to translate to or '0' to translate to all languages:"))
word = input("Type the word you want to translate:")
if lang_to != 0:
    print('You choose "{0}" as a language to translate "{1}".'.format(lang_dict[lang_to], word))

for lang_key, lang_val in lang_dict.items():
    translate_list = []
    example_list = []
    if lang_key != lang_from:
        if lang_to == 0 or (lang_to != 0 and lang_to == lang_key):
            url = "https://context.reverso.net/translation/{0}-{1}/{2}".format(lang_dict[lang_from].lower(), lang_dict[lang_key].lower(), word)
            # print(url)
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                # print(r.status_code, 'OK')
                soup = BeautifulSoup(r.content, 'html.parser')
                translate_result = soup.find(id="translations-content").find_all("a")
                for translate in translate_result:
                    # print(str(translate.text).strip())
                    translate_list.append(str(translate.text).strip())
                translate_dict[lang_dict[lang_key]] = {}
                translate_dict[lang_dict[lang_key]]['translate'] = translate_list
                example_result = soup.find(id="examples-content").find_all("span", {"class": "text"})
                for example in example_result:
                    example_list.append(example.text.strip())
                translate_dict[lang_dict[lang_key]]['example'] = example_list
print_result(translate_dict, n_translate)
save_to_file(translate_dict, n_translate, word)


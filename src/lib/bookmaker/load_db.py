from bs4 import BeautifulSoup
import simplejson
import os
import pandas as pd
import requests
import re

RELOAD_JSON = 1
HTML_INTO_JSON = 1

RESCRAPE = 1
REWRITE = 0

dir = os.path.dirname(__file__)

file_excel = os.path.join(dir, 'kb.xlsx')
file_json = os.path.join(dir, 'kiseki-books.json')

def load_excel_data(nest=True):
    games = pd.read_excel(file_excel, 'games').to_dict(orient='records')
    series = pd.read_excel(file_excel, 'series').to_dict(orient='records')
    books = pd.read_excel(file_excel, 'books').to_dict(orient='records')

    print("Data from kb.xlsx loaded.")

    if nest:
        i = 0
        j = 0

        serie = series[i]
        book = books[j]
        
        for game in games:
            game['series'] = []

            while serie['game_id'] == game['id'] and i != len(series):
                game['series'].append(serie)
                serie['books'] = []

                write_br = serie['title'] == 'Black Records'

                while book['series_id'] == serie['id'] and j != len(books):
                    serie['books'].append(book)

                    if write_br and serie['id'] != 43:
                        games[6]['series'][1]['books'].append(book)

                    j += 1
                    try: book = books[j]
                    except IndexError: pass

                i += 1
                try: serie = series[i]
                except IndexError: pass

        games[7]['series'][1]['books'] = games[6]['series'][1]['books']
        games[8]['series'][1]['books'] = games[6]['series'][1]['books']

        print("Object converted into full nest.")

        return games

    return { 'games': games, 'series': series, 'books': books }

def load_into_json(data):
    data.pop() # DAYBREAK II POP

    file = file_json

    if HTML_INTO_JSON:
        data = html_into_json(data)
        file = os.path.join(dir, 'kiseki-books-full.json')

    with open(file, 'w') as f:
        f.write(simplejson.dumps(data, indent=4, ignore_nan=True))

    print("JSON file created.")

def clean_html(html_str):
    for tag in html_str.find_all(True):
        for attr in list(tag.attrs):
            if attr != 'class' or 'spoiler' not in tag.get('class', []):
                if not (attr == 'src' and tag.name == 'img'):
                    tag.attrs.pop(attr, None)

    for spoiler in html_str.find_all('span', class_='spoiler'):
        spoiler.string = spoiler.get_text().strip()

    for img in html_str.find_all('img'):
        src = img.get('src')

        if src:
            if 'data:' in src:
                img.decompose()
                continue

            ext = re.search(r'\.(png|jpg)(?=[/?]|$)', src).group()
            img['src'] = src.split(ext)[0] + ext

        img.parent.unwrap()

        if img.find_parent('noscript'):
            img.parent.unwrap()

    for cap in html_str.find_all('figcaption'):
        for child in cap.findChildren(recursive=False):
            if child.name != 'p':
                child.extract()
            
    return str(html_str)

def wrap_tag(txt, tag, classes = ''):
    if classes:
        classes = f' class=\"{classes}\"'

    return f'<{tag}{classes}> {txt} </{tag}>'

def get_book_part(href):
    soup = BeautifulSoup(requests.get(href).content, "html.parser")
    tabbers = soup.find_all('div', class_='wds-tabber')

    UNAVAIL_EN = wrap_tag('English text not available.', 'p', 'unavailable')
    UNAVAIL_JA = wrap_tag('Japanese text not available.', 'p', 'unavailable')

    langs = {
        'en': { 'tags': ['english', 'en'], 'text': '' }, 
        'ja': { 'tags': ['japanese', 'jp', 'ja'], 'text': '' }
    }

    for exception in ['Moonless_Morn', 'Imperial_Railways', 'Beyond_Tradition', 'The_Media', 'Crossbell_Times_(Azure)']:
        if exception in href:
            chapters = soup.find_all('blockquote')
            text = ''

            for chapter in chapters:
                text += clean_html(chapter)

            if exception == 'Crossbell_Times_(Azure)':
                if href.split('/')[-1] not in ['Issue_6', 'Issue_7', 'Issue_8', 'Issue_9', 'Issue_10', 'Issue_11', 'Special_Edition']:
                    break

            if exception == 'Moonless_Morn':
                return {
                'en': UNAVAIL_EN,
                'ja': text
            }

            return {
                'en': text,
                'ja': UNAVAIL_JA
            }

    for tabber in tabbers:
        tabs = tabber.find_all('div', class_='wds-tab__content')

        if len(tabs) == 0:
            raise Exception(f"No valid tabbers found for {href}. Enter a valid Falcom book wiki link.")
        
        text_en = ''
        text_ja = ''

        if tabs[0].blockquote.text.strip() == '':
            text_en = UNAVAIL_EN
        else:
            text_en = clean_html(tabs[0].blockquote)

        if len(tabs) == 1 or tabs[1].blockquote.text.strip() == '':
            text_ja = UNAVAIL_JA
        else:
            text_ja = clean_html(tabs[1].blockquote)

        if 'Reverie' in href:
            text_ja = text_en
            text_en = UNAVAIL_EN

        langs['en']['text'] += text_en
        langs['ja']['text'] += text_ja

    return { 
        'en': langs['en']['text'], 
        'ja': langs['ja']['text']
    }

def scrape_html(data):
    WIKI = 'https://kiseki.fandom.com/wiki/'
    
    for game in data:
        print(f'\nScraping books from {game['title']}.')

        for serie in game['series']:
            folder = os.path.join(dir, 'books', serie['file'])

            if not REWRITE and os.path.isdir(folder) and serie['title'] != 'Black Records':
                print(f'Series {serie['title']} already exists, skipping.')
                continue

            for book in serie['books']:
                href = WIKI + book['wiki_slug']

                file_en = os.path.join(folder, 'en', f'{book['part']}.html')
                file_ja = os.path.join(folder, 'ja', f'{book['part']}.html')

                print(f'Scraping {serie['title']} - {book['title']}. Attemping to write...', end=' ')

                if not REWRITE and (os.path.isfile(file_en) and os.path.isfile(file_ja)):
                    print('skipped!')
                    continue

                book_text = get_book_part(href)

                os.makedirs(os.path.dirname(file_en), exist_ok=True)
                os.makedirs(os.path.dirname(file_ja), exist_ok=True)

                with open(file_en, 'w', encoding='utf-8') as f:
                    f.write(book_text['en'])

                with open(file_ja, 'w', encoding='utf-8') as f:
                    f.write(book_text['ja'])

                print("done!")
    
    print('\nFinished scraping all books.')

def html_into_json(data):
    for game in data:
        for serie in game['series']:
            folder = os.path.join(dir, 'books', serie['file'])

            for book in serie['books']:
                file_en = os.path.join(folder, 'en', f'{book['part']}.html')
                file_ja = os.path.join(folder, 'ja', f'{book['part']}.html')

                with open(file_en, 'r', encoding='utf-8') as f:
                    book['text_en'] = f.read()

                with open(file_ja, 'r', encoding='utf-8') as f:
                    book['text_ja'] = f.read()
    
    return data

    

# driver    

if __name__ == "__main__": 
    data = load_excel_data()

    if RELOAD_JSON:
        load_into_json(data)

    if RESCRAPE:
        scrape_html(data)

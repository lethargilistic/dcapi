import json
import mwclient
import re
import requests
from bs4 import BeautifulSoup

def get_character_list():
    r = requests.get('http://www.detectiveconanworld.com/wiki/Category:Characters')
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    #There should only ever be one section
    character_section = soup.find_all('div', id='mw-pages')[0]
    
    character_list = []
    for character in character_section.find_all('a')[1:]: # 1 cuts off 'Characters'
        character_list.append(character['href'][6:]) #6 cuts off /wiki/

    return character_list

def filter_infobox_entry(entry):
    #Remove comments
    entry = re.sub(r'<!--.*?-->', '', 
                    entry, 
                    re.DOTALL|re.MULTILINE) #remove comments

    #Remove references
    entry = re.sub(r'<ref.*?(?:</ref>|/>)', '', 
                    entry, 
                    re.DOTALL|re.MULTILINE) #remove comments

    #Change pipe-links to just visible text
    entry = re.sub(r'\[\[(?:.*?\|)*(.*?)\]\]', r'\1', 
                    entry, 
                    re.DOTALL|re.MULTILINE) #remove comments

    #Change language templates to just visible text
    entry = re.sub(r'\{\{lang\|(?:.*?\|)*(.*?)\}\}', r'\1', 
                    entry, 
                    re.DOTALL|re.MULTILINE) #remove comments

    return entry

NOT_CHARACTER_PAGES = {'Akai_family%27s_middle_brother', '%22The_Criminal%22', 'Scar_Akai'}
def get_infobox_json(names):
    site = mwclient.Site(('http', 'www.detectiveconanworld.com'), path='/wiki/')
    all_characters = []
    for name in names:
        if name in NOT_CHARACTER_PAGES:
            continue

        text = site.pages[name].text()
        try:
            infobox = re.search(r'\{\{InfoBox Char(.*?)\n\}\}', text, re.DOTALL|re.MULTILINE).group(1)
        except:
            print(name, 'has no infobox?')
            continue

        one_character = dict()
        for line in infobox.split('\n|'):
            
            if line:
                keyword, value = line.split('=', 1)
                keyword = keyword.strip()
                value = value.strip()
                one_character[keyword] = filter_infobox_entry(value)

        if 'age' in one_character:
            if '<br' in one_character['age']:
                one_character['age'] = one_character['age'][:one_character['age'].find('<br')]
            if '-' in one_character['age']:
                one_character['age'] = one_character['age'][:one_character['age'].find('-')]

        if 'keyhole' in one_character:
            if '<br' in one_character['keyhole']:
                one_character['keyhole'] = one_character['keyhole'][:one_character['keyhole'].find('<br')]

        all_characters.append(one_character)
    return all_characters

def prepare_json(infoboxes_list):
    fixed_list = []
    for original_dict in infoboxes_list:
        try:
            print(original_dict['name'])
            english_name = original_dict['english-name'] if original_dict['english-name'] else original_dict['name']
            if not english_name:
                english_name = None

            fixed_dict = dict()
            fixed_dict['name'] = {'japanese':{'romanized':original_dict.get('name', None),
                                              'kanji':original_dict.get('japanese-name', None)},
                                  'english':{'anime':english_name,
                                             'manga':english_name}}
            try:
                fixed_dict['age'] = int(original_dict.get('age')) if original_dict.get('age', None) else None
            except ValueError:
                fixed_dict['age'] = None
            fixed_dict['gender'] = original_dict.get('gender', None)
            fixed_dict['date_of_birth'] = original_dict.get('date-of-birth', None)
            fixed_dict['occupation'] = original_dict.get('occupation', None)
            #fixed_dict['nicknames'] = original_dict.get('nicknames', None)
            fixed_dict['aliases'] = original_dict.get('aliases', None)
            fixed_dict['image'] = original_dict.get('image', None)
            fixed_dict['first_appearance'] = {'manga':original_dict.get('first-appearance', None),
                                              'anime':original_dict.get('first-appearance', None)}
            #TODO: Figure out how many cases solved via case data. 5(6 as Subaru) is possible in infoboxes.
            #fixed_dict['cases_solved'] = int(original_dict.get('cases-solved')) if original_dict.get('cases-solved', '') else 0
            #7 cuts off the 'Volume ' in keyhole data
            try:
                fixed_dict['keyhole'] = int(original_dict.get('keyhole', 'Volume 0')[7:])
                if fixed_dict['keyhole'] == 0:
                    fixed_dict['keyhole'] = None

            except ValueError:
                fixed_dict['keyhole'] = None
            fixed_dict['voice'] = {'japanese':original_dict.get('japanese-voice', None),
                                   'english':original_dict.get('english-voice', None)},
            fixed_dict['drama_actor'] = original_dict.get('drama-actor', None)
            fixed_list.append(fixed_dict)
        except:
            import sys
            print(original_dict['name'], sys.exc_info())
            sys.exit(1)

    for i, character in enumerate(fixed_list):
        for field in character:
            if isinstance(field, str) and not character[field]:
                fixed_list[i][field] = None
    return fixed_list
 
if __name__ == '__main__':
    with open('../json/characters.json', 'r') as f:
        all_characters = json.loads(f.read())
        for character in all_characters:
            if character['image']:
                url = 'http://www.detectiveconanworld.com/wiki/File:' + character['image']
                html = requests.get(url).text

                soup = BeautifulSoup(html, 'html.parser')
                try:
                    image_link = soup.find_all('div', id='file')[0]
                except:
                    print(character['image'] + "didn't work")
                    continue
                image_link = image_link.a['href']
                url = 'http://www.detectiveconanworld.com' + image_link
                import urllib
                urllib.request.urlretrieve(url,
                        character['name']['japanese']['romanized']
                        + character['image'][-4:])
            print(character['name']['japanese']['romanized'])


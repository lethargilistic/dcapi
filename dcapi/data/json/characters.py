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
    entry = re.sub(r'<ref.*?</ref>', '', 
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

            fixed_dict = dict()
            fixed_dict['name'] = {'japanese':{'romanized':original_dict['name'],
                                              'kanji':original_dict['japanese-name']},
                                  'english':{'anime':english_name,
                                             'manga':english_name}}
            try:
                fixed_dict['age'] = int(original_dict.get('age')) if original_dict.get('age', '') else 0
            except ValueError:
                fixed_dict['age'] = 0
            fixed_dict['gender'] = original_dict.get('gender', 'Unknown')
            fixed_dict['date_of_birth'] = original_dict.get('date-of-birth', 'Unknown')
            fixed_dict['occupation'] = original_dict.get('occupation', '')
            fixed_dict['nicknames'] = original_dict.get('nicknames', '')
            fixed_dict['aliases'] = original_dict.get('aliases', '')
            fixed_dict['image'] = original_dict.get('image', '')
            fixed_dict['first_appearance'] = {'manga':original_dict['first-appearance'],
                                              'anime':original_dict['first-appearance']}
            #TODO: Figure out how many cases solved via case data. 5(6 as Subaru) is possible in infoboxes.
            #fixed_dict['cases_solved'] = int(original_dict.get('cases-solved')) if original_dict.get('cases-solved', '') else 0
            #7 cuts off the 'Volume ' in keyhole data
            try:
                fixed_dict['keyhole'] = int(original_dict.get('keyhole', 'Volume 0')[7:])
            except ValueError:
                fixed_dict['age'] = 0
            fixed_dict['voice'] = {'japanese':original_dict.get('japanese-voice', ''),
                                   'english':original_dict.get('english-voice', '')},
            fixed_dict['drama_actor'] = original_dict.get('drama-actor', '')
            fixed_list.append(fixed_dict)
        except:
            import sys
            print(original_dict['name'], sys.exc_info())
            sys.exit(1)
    return fixed_list
        
    '''
     {'name': 'Hiroshi Agasa'},
     {'japanese-name': '阿笠 博士<br>(Agasa Hiroshi)'},
     {'english-name': 'Hershel Agasa'},
     {'image': 'Hiroshi Agasa Profile.jpg'},
     {'age': '53'},
     {'gender': 'Male'},
     {'height': '160 cm (5\'3")'},
     {'date-of-birth': 'Unknown'},
     {'relatives': 'Kurisuke Agasa (great-uncle)<br>Teiko Agasa '
		   "(great-aunt)<br>Unnamed cousin<br>Unnamed cousin's "
		   'granddaughter'},
     {'occupation': 'Engineer <br /> Inventor'},
     {'aliases': 'Professor Agasa <br> Dr. Agasa'},
     {'nicknames': 'Professor (Ai Haibara) <br> Professor Agasa (Conan Edogawa, '
		   'Detective Boys)'},
     {'first-appearance': 'Manga: File 2<br />Anime: Episode 1'},
     {'appearances': '{{:Hiroshi Agasa Appearances}}'},
     {'cases-solved': ''},
     {'keyhole': 'Volume 5'},
     {'japanese-voice': 'Kenichi Ogata<br>Kazunari Tanaka (young)'},
     {'english-voice': 'Bill Flynn'},
     {'drama-actor': 'Ryosei Tayama'},
     {'footnotes': ''}]
    '''

 
if __name__ == '__main__':
    names = get_character_list()
    unprepared_json_list = get_infobox_json(names)
    final_json_list = prepare_json(unprepared_json_list)
    with open('auto-characters.json', 'w') as f:
        import json
        f.write(json.dumps(final_json_list, indent=4, sort_keys=True))

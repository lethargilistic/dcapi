import json
import logging
import os.path
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

from .models import Character

def build_characters(db):
    log.log(logging.INFO, "build_characters")
    with open(os.path.join(os.path.dirname(__file__), 'data/json/auto-characters.json'), 'r') as datafile:
        characters_dict = json.loads(datafile.read())

    Character.all().delete()
    for index, char in enumerate(characters_dict):
        if 'keyhole' not in char:
            print(char['name'])
        parameters = dict(
            id=index,
            age=char['age'],
            aliases=char['aliases'],
            date_of_birth=char['date_of_birth'],
            drama_actor=char['drama_actor'],

            manga_first_appearance=char['first_appearance']['manga'],
            anime_first_appearance=char['first_appearance']['anime'],
            
            gender='Female' if char['gender'] == 'F' else 'Male',
            keyhole=char['keyhole'],

            english_anime_name=char['name']['english']['anime'],
            english_manga_name=char['name']['english']['manga'],
            kanji_name=char['name']['japanese']['kanji'],
            romanized_name=char['name']['japanese']['romanized'],

            occupation=char['occupation'],
            japanese_voice=char['voice'][0]['japanese'], #FIXME: I have no idea why these are arrays. This is a cludge.
            english_voice=char['voice'][0]['english'],
        )
        row = Character.create(**parameters)
        log.log(logging.INFO, str(row) + " : " + parameters['romanized_name'])

    db.commit()

def build_all(db):
    log.log(logging.INFO, "build_all")
    build_characters(db)

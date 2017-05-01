import json

from models import Character

def build_characters(db):
    with open('data/json/characters.json', 'r') as datafile:
        characters_dict = json.loads(datafile.read())

    Character.all().delete()
    for char in characters_dict:
        parameters = dict(
            id=char['id'],
            kanji_name=char['name']['japanese']['kanji'],
            romanized_name=char['name']['japanese']['romanized'],
            english_anime_name=char['name']['english']['anime'],
            english_manga_name=char['name']['english']['manga'],
            age=char['age'],
            date_of_birth=char['date_of_birth'],
            gender='Female' if char['gender'] == 'F' else 'Male',
            occupation=char['occupation'],
            manga_first_appearance=char['first_appearance']['manga'],
            anime_first_appearance=char['first_appearance']['anime'],
            cases_solved=char['cases_solved'],
            keyhole=char['keyhole'],
            japanese_voice=char['voice']['japanese'],
            english_voice=char['voice']['english'],
            drama_actor=char['drama_actor'],
        )
        Character.create(**parameters)

    db.commit()

def build_all(db):
    build_characters(db)

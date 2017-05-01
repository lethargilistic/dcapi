import json

from weppy import App
from weppy.tools import service
from weppy.orm import Database, Model, Field
from weppy.sessions import SessionCookieManager

from keys import DB_PIPE_KEY
from models import Character

app = App(__name__)

db = Database(app, auto_migrate=True)
db.define_models(Character)

def build_characters():
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

@app.command('setup')
def setup():
    build_characters()

app.pipeline = [
    SessionCookieManager(DB_PIPE_KEY), db.pipe
]

@app.route('/')
def there_is_always_one_truth():
    return "真実はいつもひとつ！"

@app.route('/character/<int:character_id>')
@service.json
def character(character_id):
    return db(Character.id == character_id).select().first()
   


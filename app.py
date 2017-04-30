import json

from weppy import App
from weppy.tools import service
from weppy.orm import Database, Model, Field
from weppy.sessions import SessionCookieManager

app = App(__name__)

class Character(Model):
    id = Field()
    name = Field('text')

db = Database(app, auto_migrate=True)
db.define_models(Character)

def build_characters():
    with open('data/json/characters.json', 'r') as datafile:
        characters_dict = json.loads(datafile.read())
    for char in characters_dict:
        Character.all().delete()
        character = Character.create(id=char['id'], name=char['name']['japanese']['kanji'])
    for c in Character.all().select():
        print(c.name)
        d = dir(db(Character.id == 1).select())
        print(d)
        ch = db(Character.id == 1).select().as_dict()
        print(ch)
    db.commit()

@app.command('setup')
def setup():
    build_characters()

app.pipeline = [
    SessionCookieManager('Walternate'), db.pipe
]

@app.route('/')
def there_is_always_one_truth():
    return "真実はいつもひとつ！"

@app.route('/character/<int:character_id>')
@service.json
def character(character_id):
    return db(Character.id == character_id).select().first()
   


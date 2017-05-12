import json

from weppy import App
from weppy.tools import service
from weppy.orm import Database, Model, Field
from weppy.sessions import SessionCookieManager

from build import build_all
from keys import DB_PIPE_KEY
from models import Character

app = App(__name__)

db = Database(app, auto_migrate=True)
db.define_models(Character)

@app.command('setup')
def setup():
    build_all(db)

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
   
@app.route('/character/<str:name>')
@service.json
def search_character(name):

    roman = db(Character.romanized_name == name).select().first()
    if roman:
        return {**{'status':200}, **roman}

    english_anime = db(Character.english_anime_name == name).select().first()
    if english_anime:
        return {**{'status':200}, **english_anime}

    english_manga = db(Character.english_manga_name == name).select().first()
    if english_manga:
        return {**{'status':200}, **(english_manga.as_dict())}

    kanji = db(Character.kanji_name == name).select().first()
    if kanji:
        return {**{'status':200}, **(kanji.as_dict())}

    return {'status': 404, 'message':'Character not found'}

import json

from weppy import App, abort
from weppy.tools import service
from weppy.orm import Database, Model, Field
from weppy.sessions import SessionCookieManager

from .build import build_all
from .keys import DB_PIPE_KEY
from .models import Character

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

@app.route('/character/<int:character_id>', methods="get")
@service.json
def character(character_id):
    return db(Character.id == character_id).select().first()
   
@app.route('/character/<str:name>', methods="get")
@service.json
def search_character_together(name):
    char = db((Character.romanized_name == name) 
               | (Character.english_anime_name == name)
               | (Character.english_manga_name == name)
               | (Character.kanji_name == name)).select().first()
    if char:
        return char.as_dict()

    return abort(404)

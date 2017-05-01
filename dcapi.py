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
   


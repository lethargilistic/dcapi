import json

from weppy import App
from weppy.tools import service
app = App(__name__)

with open('data/json/characters.json', 'r') as datafile:
    characters_dict = json.loads(datafile.read())

@app.route('/')
def hello():
    return "There is one truth!"

@app.route('/character/<int:character_id>')
@service.json
def character(character_id):
    return characters_dict[character_id-1]

if __name__ == "__main__":
    app.run()

from weppy.orm import Model, Field

class Character(Model):
   id = Field()
   kanji_name = Field('text')
   romanized_name = Field('text')
   english_anime_name = Field('text')
   english_manga_name = Field('text')
   age = Field('int')
   gender = Field('text')
   date_of_birth = Field('text')
   occupation = Field()
   manga_first_appearance = Field('int')
   anime_first_appearance = Field('int')
   cases_solved = Field('int')
   keyhole = Field('int')
   japanese_voice = Field('text')
   english_voice = Field('text')
   drama_actor = Field('text')

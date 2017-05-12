from weppy.orm import Model, Field

class Character(Model):
   id = Field()
   kanji_name = Field('text')
   romanized_name = Field('text')
   english_anime_name = Field('text', validation={'allow':'blank'})
   english_manga_name = Field('text', validation={'allow':'blank'})
   age = Field('int', validation={'allow':'blank'})
   gender = Field('text')
   date_of_birth = Field('text')
   occupation = Field()
   manga_first_appearance = Field('int')
   anime_first_appearance = Field('int', validation={'allow':'blank'})
   cases_solved = Field('int')
   keyhole = Field('int', validation={'allow':'blank'})
   japanese_voice = Field('text')
   english_voice = Field('text', validation={'allow':'blank'})
   drama_actor = Field('text', validation={'allow':'blank'})

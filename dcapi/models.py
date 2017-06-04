from weppy.orm import Model, Field

class Character(Model):
   id = Field()
   age = Field('int', validation={'allow':'blank'})
   aliases = Field('text')
   date_of_birth = Field('text', validation={'allow':'blank'})
   drama_actor = Field('text', validation={'allow':'blank'})

   #TODO: Should be int, but not going to parse it out right now
   manga_first_appearance = Field('text', validation={'allow':'blank'})
   anime_first_appearance = Field('text', validation={'allow':'blank'})
   
   gender = Field('text', validation={'allow':'blank'})
   keyhole = Field('int', validation={'allow':'blank'})

   english_anime_name = Field('text', validation={'allow':'blank'})
   english_manga_name = Field('text', validation={'allow':'blank'})
   kanji_name = Field('text')
   romanized_name = Field('text')

   occupation = Field('text', validation={'allow':'blank'})
   japanese_voice = Field('text', validation={'allow':'blank'})
   english_voice = Field('text', validation={'allow':'blank'})

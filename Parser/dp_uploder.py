import json
from models import *

with open('animes.txt', encoding='utf-8') as f:
    animes = json.loads(f.read())

TitlesModel.create_table()
TitlesNamesModel.create_table()
TitlesDescriptionsModel.create_table()
PlayersModel.create_table()
PlayersModel.create(players_login='admin', players_pass_hash='admin').save()
PlayersModel.create(players_login='user', players_pass_hash='user').save()

for anime in animes:
    print(anime['names'][0])
    title = TitlesModel.create(titles_type=0, titles_subtype=anime['subtype'], titles_shikimori_id=anime['id'],
                titles_rating=anime['raiting'], titles_has_description=len(anime['description']) != 0)
    title.save()

    for name in anime['names']:
        TitlesNamesModel.create(titles_names_title_id=title.titles_id, titles_names_name=name).save()

    TitlesDescriptionsModel.create(titles_descriptions_title_id=title.titles_id,
                            titles_descriptions_descriptions_text=anime['description']).save()

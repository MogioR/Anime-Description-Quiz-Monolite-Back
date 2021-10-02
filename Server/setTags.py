#Set tegs for bd

from models import *
import json

query1 = TitlesNamesModel.select(TitlesNamesModel.titles_names_name).join(TitlesModel, JOIN.INNER).join(TitlesGenresModel, JOIN.INNER)\
    .where(TitlesGenresModel.titles_genres_genre_family_id == 25)
query2 = TitlesNamesModel.select(TitlesNamesModel.titles_names_name).join(TitlesModel, JOIN.INNER).join(TitlesGenresModel, JOIN.INNER)\
    .where(TitlesGenresModel.titles_genres_genre_family_id == 18)
query = query1 & query2

print(query)
i = 1
for q in query:
    print(q.titles_names_name)

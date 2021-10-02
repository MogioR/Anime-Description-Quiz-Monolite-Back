from peewee import *
from datetime import datetime
from passwords import *
pg_db = PostgresqlDatabase('adq', user=DATABASE_LOGIN, password=DATABASE_PASS,
                           host='localhost', port=5432)

class BaseModel(Model):
    class Meta:
        database = pg_db

class PlayersModel(BaseModel):
    players_id = IdentityField()
    players_login = CharField(null=False, max_length=32, unique=True)
    players_pass_hash = CharField(null=False, max_length=128)
    players_exp = IntegerField(null=False, default=0)
    players_speshal_points = IntegerField(null=False, default=0)

    players_true_answers = IntegerField(null=False, default=0)
    players_rounds_played = IntegerField(null=False, default=0)

    players_registration = DateField(null=False, default=datetime.now())
    players_last_login = DateField(null=False, default=datetime.now())
    players_is_baned = BooleanField(null=False, default=False)

    players_shikimori_login = CharField(null=True, max_length=128)
    players_mal_login = CharField(null=True, max_length=128)
    players_anilist_login = CharField(null=True, max_length=128)

    class Meta:
        db_table = "players"
        order_by = ('players_id',)

class FriendsListModel(BaseModel):
    friends_list_id_player = ForeignKeyField(PlayersModel, backref='players', to_field='players_id', on_delete='cascade',
                               on_update='cascade')
    friends_list_id_friend = ForeignKeyField(PlayersModel, backref='players', to_field='players_id', on_delete='cascade',
                               on_update='cascade')
    class Meta:
        db_table = "friends_list"
        primary_key = CompositeKey('friends_list_id_player', 'friends_list_id_friend')

class TitlesModel(BaseModel):
    titles_id = IdentityField()
    titles_type = SmallIntegerField(null=False) #0-anime, 1-manga, 2-ranobe
    titles_subtype = FixedCharField(null=False, max_length=32)
    titles_shikimori_id = FixedCharField(null=False, max_length=20)

    titles_creation_date = DateField(null=False, default=datetime.now())
    titles_rating = FloatField(null=False, default=0)

    titles_has_description = BooleanField(null=False, default=False)
    titles_has_pictures = BooleanField(null=False, default=False)
    titles_has_music = BooleanField(null=False, default=False)

    class Meta:
        db_table = "titles"
        order_by = ('titles_id',)

class GenresModel(BaseModel):
    genres_id = IdentityField()
    genres_family_id = SmallIntegerField(null=False)
    genres_name = CharField(null=False, max_length=32)
    genres_language = SmallIntegerField(null=False, default=0) #0-ru, 1-eng

    class Meta:
        db_table = "genres"

class TitlesNamesModel(BaseModel):
    titles_names_id = IdentityField()
    titles_names_title_id = ForeignKeyField(TitlesModel, backref='titles', to_field='titles_id', on_delete='cascade',
                               on_update='cascade')
    titles_names_name = CharField(null=False, max_length=128)
    titles_names_language = SmallIntegerField(null=False, default=0)  # 0-ru, 1-eng

    class Meta:
        db_table = "titles_names"

class TitlesGenresModel(BaseModel):
    titles_genres_id = IdentityField()
    titles_genres_genre_family_id = SmallIntegerField(null=False)
    titles_genres_title_id = ForeignKeyField(TitlesModel, backref='titles', to_field='titles_id', on_delete='cascade',
                               on_update='cascade')

    class Meta:
        db_table = "titles_genres"

class TitlesListModel(BaseModel):
    titles_list_id_player = ForeignKeyField(PlayersModel, backref='players', to_field='players_id', on_delete='cascade',
                               on_update='cascade')
    titles_list_id_title = ForeignKeyField(TitlesModel, backref='titles', to_field='titles_id', on_delete='cascade',
                               on_update='cascade')
    class Meta:
        db_table = "titles_list"
        primary_key = CompositeKey('titles_list_id_player', 'titles_list_id_title')

class TitlesDescriptionsModel(BaseModel):
    titles_descriptions_id = IdentityField()
    titles_descriptions_title_id = ForeignKeyField(TitlesModel, backref='titles', to_field='titles_id', on_delete='cascade',
                               on_update='cascade')
    titles_descriptions_language = SmallIntegerField(null=False, default=0)  # 0-ru, 1-eng
    titles_descriptions_descriptions_text = TextField(null=False)

    titles_descriptions_true_answers = IntegerField(null=False, default=0)
    titles_descriptions_round_played = IntegerField(null=False, default=0)

    class Meta:
        db_table = "titles_descriptions"

class TitlesPicturesModel(BaseModel):
    titles_pictures_id = IdentityField()
    titles_pictures_title_id = ForeignKeyField(TitlesModel, backref='titles', to_field='titles_id', on_delete='cascade',
                               on_update='cascade')
    titles_pictures_pictures_url = TextField(null=False)

    titles_pictures_true_answers = IntegerField(null=False, default=0)
    titles_pictures_round_played = IntegerField(null=False, default=0)

    class Meta:
        db_table = "titles_pictures"


class TitlesMusicsModel(BaseModel):
    titles_musics_id = IdentityField()
    titles_musics_title_id = ForeignKeyField(TitlesModel, backref='titles', to_field='titles_id', on_delete='cascade',
                                               on_update='cascade')
    titles_musics_musics_url = TextField(null=False)

    titles_musics_true_answers = IntegerField(null=False, default=0)
    titles_musics_round_played = IntegerField(null=False, default=0)

    class Meta:
        db_table = "titles_musics"


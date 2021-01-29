from peewee import *
from datetime import datetime

pg_db = PostgresqlDatabase('postgres', user='', password='',
                           host='localhost', port=5432)

class BaseModel(Model):
    class Meta:
        database = pg_db


class Player(BaseModel):
    id = PrimaryKeyField(null=False)
    p_name = CharField(null=False, max_length=32, unique=True)
    p_pass_hash = CharField(null=False, max_length=128)
    p_exp = IntegerField(null=False, default=0)
    p_points = IntegerField(null=False, default=0)
    p_true_answers = IntegerField(null=False, default=0)
    p_round_played = IntegerField(null=False, default=0)
    p_registration = DateField(null=False, default=datetime.now())

    class Meta:
        db_table = "players"
        order_by = ('id',)

class Friends(BaseModel):
    id_p = ForeignKeyField(Player, backref='players', to_field='id', on_delete='cascade',
                               on_update='cascade')
    id_f = ForeignKeyField(Player, backref='players', to_field='id', on_delete='cascade',
                               on_update='cascade')
    class Meta:
        db_table = "friends"
        primary_key = CompositeKey('id_p', 'id_f')

class Film(BaseModel):
    id = PrimaryKeyField(null=False)
    f_url = TextField(null=False)
    f_creation_date = DateField(null=False)
    f_true_answers = IntegerField(null=False, default=0)
    f_round_played = IntegerField(null=False, default=0)
    f_rating = FloatField(null=False, default=5)

    class Meta:
        db_table = "films"
        order_by = ('id',)

class Gener(BaseModel):
    id = PrimaryKeyField(null=False)
    g_name = CharField(null=False, max_length=128)

    class Meta:
        db_table = "generes"


class Tag(BaseModel):
    id = PrimaryKeyField(null=False)
    t_name = CharField(null=False, max_length=128)

    class Meta:
        db_table = "tags"

class Film_name(BaseModel):
    id = PrimaryKeyField(null=False)
    film_id = ForeignKeyField(Film, backref='films', to_field='id', on_delete='cascade',
                               on_update='cascade')
    f_name = CharField(null=False, max_length=128)
    class Meta:
        db_table = "film_names"

class Film_tag(BaseModel):
    id_f = ForeignKeyField(Film, backref='films', to_field='id', on_delete='cascade',
                               on_update='cascade')
    id_t = ForeignKeyField(Tag, backref='tags', to_field='id', on_delete='cascade',
                               on_update='cascade')
    class Meta:
        db_table = "film_tags"
        primary_key = CompositeKey('id_f', 'id_t')

class Film_genere(BaseModel):
    id_f = ForeignKeyField(Film, backref='films', to_field='id', on_delete='cascade',
                               on_update='cascade')
    id_g = ForeignKeyField(Gener, backref='generes', to_field='id', on_delete='cascade',
                               on_update='cascade')
    class Meta:
        db_table = "film_genres"
        primary_key = CompositeKey('id_f', 'id_g')

class Player_film(BaseModel):
    id_p = ForeignKeyField(Player, backref='players', to_field='id', on_delete='cascade',
                               on_update='cascade')
    id_f = ForeignKeyField(Film, backref='films', to_field='id', on_delete='cascade',
                               on_update='cascade')
    class Meta:
        db_table = "player_films"
        primary_key = CompositeKey('id_p', 'id_f')

class Player_reqest(BaseModel):
    id = PrimaryKeyField(null=False)
    req_id_p = ForeignKeyField(Player, backref='players', to_field='id', on_delete='cascade',
                           on_update='cascade')
    req_req_f = ForeignKeyField(Film, backref='films', to_field='id', on_delete='cascade',
                               on_update='cascade')
    req_true_f = ForeignKeyField(Film, backref='films', to_field='id', on_delete='cascade',
                               on_update='cascade')
    req_time = FloatField(null=False)
    class Meta:
        db_table = "player_reqests"

class Game(BaseModel):
    id = PrimaryKeyField(null=False)
    g_type = IntegerField(null=False, default=0)
    class Meta:
        db_table = "games"

class Game_reqest(BaseModel):
    id_rec = ForeignKeyField(Player_reqest, backref='player_reqests', to_field='id', on_delete='cascade',
                               on_update='cascade')
    id_g = ForeignKeyField(Game, backref='games', to_field='id', on_delete='cascade',
                               on_update='cascade')
    class Meta:
        db_table = "games_reqests"
        primary_key = CompositeKey('id_rec', 'id_g')

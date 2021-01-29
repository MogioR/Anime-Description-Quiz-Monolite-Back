from models import *

class PlayerData:
    def __init__(self, socket, nickname):
        self.socket = socket
        self.nickname = nickname
        p = Player.select().where(Player.p_name == nickname).get()
        self.id = p.id
        self.exp = p.p_exp
        self.points = p.p_points
        self.round_played = p.p_round_played
        self.true_answers = p.p_true_answers
        self.registration = p.p_registration
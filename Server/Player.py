from Server.models import *

class Player:
    def __init__(self, socket, nickname):
        self.nickname = nickname
        self.currentAnswer = ""
        p = PlayerModel.select().where(PlayerModel.p_name == nickname).get()
        self.id = p.id
        self.exp = p.p_exp
        self.points = p.p_points
        self.roundPlayed = p.p_round_played
        self.trueAnswers = p.p_true_answers
        self.registrationDate = p.p_registration
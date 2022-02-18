from models import *

START_PLAYER_STATE = "lobby_list"


class Player:
    def __init__(self, player):
        self.currentAnswer = ""

        self.nickname = player.players_login
        self.id = player.players_id
        self.exp = player.players_exp
        self.points = player.players_speshal_points
        self.roundPlayed = player.players_rounds_played
        self.trueAnswers = player.players_true_answers
        self.registrationDate = player.players_registration
        self.state = {'screen': START_PLAYER_STATE, 'screen_id': -1}


from Server.models import *

START_PLAYER_STATE = "lobbySearch"

class Player:
    def __init__(self, player):
        self.state = START_PLAYER_STATE
        self.currentAnswer = ""

        self.nickname = player.p_name
        self.id = player.id
        self.exp = player.p_exp
        self.points = player.p_points
        self.roundPlayed = player.p_round_played
        self.trueAnswers = player.p_true_answers
        self.registrationDate = player.p_registration


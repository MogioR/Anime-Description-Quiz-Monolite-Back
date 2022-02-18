import asyncio
import json
from Question import Qestion
from serverUtilites import *

PHASE_TIMER = 30
DEFAULT_GAME_SETTINGS = {
    'name': '',
    'password': '',
    'question_phase_time': 20,
    'answer_phase_time': 5,
    'question_types': ['description'],
    'game_mode': 'default',
    'only_anime_lists': False,
    'min_rating': 0,
    'max_rating': 10,
    'round_count': 100,
}


class Lobby:
    def __init__(self, host_name, host_socket, size, id):
        self.host = host_name
        self.host_socket = host_socket
        self.size = size
        self.players = []
        self.sockets = []
        self.playersData = []
        self.timer = 0
        self.phase = 0
        self.question = Qestion()
        self.id = id
        self.state = 'in_lobby'
        self.round = 0
        self.gameSettings = DEFAULT_GAME_SETTINGS

    def connect(self, player, socket, messageQueue):
        self.players.append(player)
        self.sockets.append(socket)
        player.state['screen'] = 'in_lobby'
        player.state['screen_id'] = self.id

        self.playersData.append({
            'name': player.nickname,
            'level': int(player.exp/1000),
            'id': player.id,
            'score': 0,
            'answer': '',
        })

        message = json.dumps({'action': 'lobby', 'type': 'setPlayerList',
                              'players': self.playersData})
        notifySockets(self.sockets, message, messageQueue)
        messageQueue.append(Package(socket, json.dumps({'action': 'lobby', 'type': 'enter'})))
        messageQueue.append(Package(socket, self.create_settings_message()))

    def start(self):
        self.phase = 1
        self.timer = 0
        self.round = 0
        self.state = 'in_game'

    def stop(self):
        self.phase = 0
        self.timer = 0

    def disconnect(self, socket, messageQueue):
        if socket in self.sockets:
            print('Disconnected from lobby')
            index = self.sockets.index(socket)
            self.sockets.pop(index)
            notifySockets(self.sockets, json.dumps({'action': 'lobby', 'type': 'playerDisconnect',
                                                    'player': self.players[index]}), messageQueue)

            self.players.pop(index)
            self.playersData.pop(index)
            if socket == self.host_socket and len(self.sockets) > 0:
                self.host_socket = self.sockets[0]
                self.host = self.players[0]

    def create_settings_message(self):
        message = json.dumps({'action': 'lobby', 'type': 'setLobbySettings', 'settings': self.gameSettings})
        return message

    def setAnswer(self, socket, answer):
        if socket in self.sockets:
            index = self.sockets.index(socket)
            self.playersData[index]['answer'] = answer

    def get_check_answers_message(self):
        answers = []
        for data in self.playersData:
            answers.append({
                'answer': data['answer'],
                'answerCheck': self.question.check_answer(data['answer'])
            })
            data['answer'] = ''
        return json.dumps({'action': 'game', 'type': 'updateAnswers', 'data': answers})

    @staticmethod
    def get_end_game_message():
        return json.dumps({'action': 'game', 'type': 'returnToLobby'})

    async def update(self, messageQueue):
        self.timer = self.timer - 1
        if self.timer <= 0:
            if self.phase == 0:
                self.timer = 0
            elif self.phase == 1:
                self.timer = 0
                await self.question.getNewQestion()
                self.phase = self.phase + 1
            elif self.phase == 2:
                self.timer = self.gameSettings['question_phase_time']
                self.phase = self.phase + 1
                notifySockets(self.sockets, self.question.getQestionMessage(), messageQueue)
                self.round += 1
            elif self.phase == 3:
                self.timer = self.gameSettings['answer_phase_time']
                self.phase = self.phase + 1
                notifySockets(self.sockets, self.question.getAnswerMessage(), messageQueue)
                notifySockets(self.sockets, self.get_check_answers_message(), messageQueue)
            else:
                if self.round < self.gameSettings['round_count']:
                    self.phase = 1
                else:
                    message = json.dumps({'action': 'lobby', 'type': 'setPlayerList', 'players': self.playersData})
                    notifySockets(self.sockets, message, messageQueue)
                    notifySockets(self.sockets, self.get_end_game_message(), messageQueue)
                    self.phase = 0

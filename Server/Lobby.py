class Lobby:
    def __init__(self, host_name,  host_socket, size):
        self.host = host_name
        self.size = size
        self.occupancy = 1
        self.players = [host_name]
        self.sockets = [host_socket]
        self.timer = 0
        self.phase = 0

    def connect(self, player, socket):
        self.players.append(player)
        self.occupancy += 1
        self.sockets.append(socket)

    def disconnect(self, player):
        self.players = [x for ind, x in enumerate(self.players) if x!=player]
        self.occupancy -= 1

    #def update(self):

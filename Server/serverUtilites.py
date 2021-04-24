from Package import Package

def notifySockets(sockets, message, messageQueue):
    for socket in sockets:
        messageQueue.append(Package(socket, message))
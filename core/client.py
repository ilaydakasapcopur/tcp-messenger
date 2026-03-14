import socket

def start_client_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
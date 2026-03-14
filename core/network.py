import json
import threading
import socket
from .server import start_server_socket
from .client import start_client_socket

class NetworkNode:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.conn = None
        self.sock = None
        self.logger = None

    def initialize_server(self):
        # start_server_socket function should return the socket object
        self.sock = start_server_socket(self.host, self.port)
        self.conn, addr = self.sock.accept()
        return addr

    def initialize_client(self):
        self.sock = start_client_socket()
        self.sock.connect((self.host, self.port))

    def start_receiver(self):
        def listen():
            # Use conn for server side, sock for client side to receive messages
            target = self.conn if self.conn else self.sock
            while True:
                try:
                    data = target.recv(4096).decode('utf-8')
                    if not data: 
                        break
                    msg = json.loads(data)
                    self.logger.add_log(msg['type'], msg['params'])
                    # Print notification to console (Standard print used as this runs in a thread)
                    print(f"\n[!] New message received ({msg['type']}). Check the logs.")
                except:
                    break
        
        threading.Thread(target=listen, daemon=True).start()

    def send_data(self, msg_type, params):
        target = self.conn if self.conn else self.sock
        if target:
            payload = json.dumps({"type": msg_type, "params": params})
            target.sendall(payload.encode('utf-8'))
            # Log the message we sent locally as well
            self.logger.add_log(msg_type, params)
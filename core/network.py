import json
import threading
import socket
from .server import start_server_socket
from .client import start_client_socket

class NetworkNode:
    def __init__(self, host='0.0.0.0', port=65432):
        self.host = host
        self.port = port
        self.conn = None
        self.sock = None
        self.logger = None
        self.saved_params = {}

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
                    self.logger.add_log(msg['type'], msg['params'], direction="received")
                    # Print notification to console (Standard print used as this runs in a thread)
                    print(f"\n[!] New message received ({msg['type']}). Check the logs.")
                    # Extract remaining turns from message (default to 0 if not present)
                    remaining_turns = msg.get('remaining_turns', 0)
                    turn_phase = msg.get('turn_phase', 'request')
                    # Trigger auto-response with the other message type
                    self._auto_respond(msg['type'], remaining_turns, turn_phase)
                except:
                    break

        threading.Thread(target=listen, daemon=True).start()

    def _auto_respond(self, received_msg_type, remaining_turns, turn_phase):
        """Auto-respond with the opposite message type as part of conversation loop."""
        import time

        # Only respond if there are remaining turns
        if remaining_turns <= 0:
            print("[Conversation loop completed - no more turns remaining]")
            return

        if received_msg_type == "MESSAGE_TYPE_1":
            response_type = "MESSAGE_TYPE_2"
        elif received_msg_type == "MESSAGE_TYPE_2":
            response_type = "MESSAGE_TYPE_1"
        else:
            return

        response_params = self.saved_params.get(response_type)
        if not response_params:
            print(f"[Warning] No saved params for {response_type}. Auto-response skipped.")
            return

        normalized_phase = turn_phase if turn_phase in {"request", "response"} else "request"
        if normalized_phase != turn_phase:
            print(f"[Warning] Unknown turn phase '{turn_phase}', defaulting to 'request'.")

        if normalized_phase == "response":
            new_turns = remaining_turns - 1
            if new_turns <= 0:
                print("[Conversation loop completed - no more turns remaining]")
                return
            next_phase = "request"
        else:
            new_turns = remaining_turns
            next_phase = "response"

        print(f"[Auto-response in 10 seconds... ({new_turns} turn(s) remaining)]")
        time.sleep(10)  # 10 second delay before auto-response

        self.send_data(response_type, response_params, remaining_turns=new_turns, turn_phase=next_phase)
        print(f"[Auto-response sent: {response_type} | Remaining turns: {new_turns}]")

    def send_data(self, msg_type, params, remaining_turns=0, turn_phase="request"):
        target = self.conn if self.conn else self.sock
        if target:
            # Save params for future auto-responses
            self.saved_params[msg_type] = params

            payload = json.dumps({
                "type": msg_type,
                "params": params,
                "remaining_turns": remaining_turns,
                "turn_phase": turn_phase
            })
            target.sendall(payload.encode('utf-8'))
            # Log the message we sent locally as well
            self.logger.add_log(msg_type, params, direction="sent")
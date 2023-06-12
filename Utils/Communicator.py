import json
import socket


from Entity.Command import CommandRequest, CommandResult


class PipeClient:
    __instance = None

    @staticmethod
    def get_instance():
        if PipeClient.__instance is None:
            PipeClient.__instance = PipeClient()
        return PipeClient.__instance

    def __init__(self):
        self.end_point = "127.0.0.1"
        self.port = 545
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.end_point, self.port))

    def send(self, request: CommandRequest):
        message = json.dumps(request.__dict__)
        encoded_message = message.encode()
        length = len(encoded_message)
        encoded_message = message.encode()
        self.socket.send(length.to_bytes(4, byteorder='little'))
        self.socket.send(encoded_message)

    def receive(self) -> CommandResult:
        # Read the length of the server's response from the Named Pipe
        response_length = int.from_bytes(self.socket.recv(4), byteorder='little')

        # Read the server's response from the Named Pipe
        response = self.socket.recv(response_length).decode().strip()

        # Deserialize the json to a CommandResult object
        response = json.loads(response)
        response = CommandResult(response['Type'], response['Message'])

        return response

    def send_and_receive(self, request: CommandRequest) -> CommandResult:
        self.send(request)
        return self.receive()

    def close(self):
        self.socket.close()

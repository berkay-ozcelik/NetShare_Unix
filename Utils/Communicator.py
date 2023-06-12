import json

import win32file

from Entity.Command import CommandRequest, CommandResult


class PipeClient:
    __instance = None

    @staticmethod
    def get_instance():
        if PipeClient.__instance is None:
            PipeClient.__instance = PipeClient()
        return PipeClient.__instance

    def __init__(self):
        self.pipe_name = r'\\.\pipe\NetShare'
        self.handle = win32file.CreateFile(
            self.pipe_name,
            win32file.GENERIC_READ | win32file.GENERIC_WRITE,
            0,
            None,
            win32file.OPEN_EXISTING,
            0,
            None
        )

    def send(self, request: CommandRequest):
        # Serialize the CommandRequest object to json
        message = json.dumps(request.__dict__)

        encoded_message = message.encode()
        length = len(encoded_message)

        # Send the length of the message to the server
        win32file.WriteFile(self.handle, length.to_bytes(4, byteorder='little'))
        # Write the message to the Named Pipe
        win32file.WriteFile(self.handle, encoded_message)

    def receive(self) -> CommandResult:
        # Read the length of the server's response from the Named Pipe
        response_length = int.from_bytes(win32file.ReadFile(self.handle, 4)[1], byteorder='little')

        # Read the server's response from the Named Pipe
        response = win32file.ReadFile(self.handle, response_length)[1].decode().strip()

        # Deserialize the json to a CommandResult object
        response = json.loads(response)
        response = CommandResult(response['Type'], response['Message'])

        return response

    def send_and_receive(self, request: CommandRequest) -> CommandResult:
        self.send(request)
        return self.receive()

    def close(self):
        win32file.CloseHandle(self.handle)

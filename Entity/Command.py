class CommandResult:
    def __init__(self, result_type, message):
        self.Type = result_type
        self.Message = message


class CommandRequest:
    def __init__(self, command, param):
        self.CommandName = command
        self.Parameter = param

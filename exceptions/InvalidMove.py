"""
File for the InvalidMove exception. This exception is raised when a move is invalid.
""" 

class InvalidMove(Exception):
    def __init__(self, message) -> None:
        self.message = message
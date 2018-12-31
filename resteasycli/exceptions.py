class FileNotFoundException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

class FileExtensionNotSupportedException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

class MethodNotAllowedException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

class EntryNotFoundException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

class InvalidCommandException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

#TODO: add file reading checks and exceptions

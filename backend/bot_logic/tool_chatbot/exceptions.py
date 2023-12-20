class LeavingChat(Exception):
    """Exception raised when the user wants to leave the chat."""

    pass


class ChatToolError(Exception):
    """Exception raised when an error occurs when calling the chat tools."""

    pass


class MissingArgumentError(Exception):
    """Exception raised when a required argument is missing."""

    pass


class InvalidClientError(Exception):
    pass

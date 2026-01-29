class AgentError(Exception):
    """Base class for all agent errors."""
    pass

class TransientError(AgentError):
    """
    Errors that might go away if we try again later.
    Examples: Network timeouts, 503 Service Unavailable.
    """
    pass

class PermanentError(AgentError):
    """
    Errors that will NOT go away.
    Examples: 401 Unauthorized, 400 Bad Request.
    """
    pass
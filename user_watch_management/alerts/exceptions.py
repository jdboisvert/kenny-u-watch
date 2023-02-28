
class SubscriptionFailureException(Exception):
    """Exception raised when a subscription fails to be created or updated."""

    def __init__(self, message):
        self.message = message

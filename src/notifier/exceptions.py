class NoOneFoundException(Exception):
    """ Exception for when no one is found """
    pass

class FailureToSendEmailException(Exception):
    """ Exception for when the email fails to send """
    pass

class FailureToConnectToSNSException(Exception):
    """ Exception for when connection to SNS fails """
    pass
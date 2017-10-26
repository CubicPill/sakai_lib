class SakaiException(Exception):
    """
    Parent class of all exceptions related to Sakai
    """
    pass


class NotLoggedIn(SakaiException):
    pass


class NoSuchItem(SakaiException):
    pass

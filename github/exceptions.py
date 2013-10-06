class GithubException(Exception):
    pass


class BadVerificationCode(GithubException):
    """
    This happens if we send an invalid or already consumed OAuth code.
    """

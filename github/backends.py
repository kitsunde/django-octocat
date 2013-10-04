from django.contrib.auth.backends import ModelBackend
from utils import get_user_model

User = get_user_model()


class GithubBackend(ModelBackend):
    """
    This backend is to be used in conjunction with the ``RemoteUserMiddleware``
    found in the middleware module of this package, and is used when the server
    is handling authentication outside of Django.

    By default, the ``authenticate`` method creates ``User`` objects for
    usernames that don't already exist in the database.  Subclasses can disable
    this behavior by setting the ``create_unknown_user`` attribute to
    ``False``.
    """

    # Create a User object if not already in the database?
    create_unknown_user = True

    def authenticate(self, github_user):
        """
        The github.models.User passed as ``github_user`` is considered trusted.
        This method simply returns the ``User`` object with the given username,
        creating a new ``User`` object if ``create_unknown_user`` is ``True``.

        Returns None if ``create_unknown_user`` is ``False`` and a ``User``
        object with the given username is not found in the database.
        """
        if not github_user:
            return

        if self.create_unknown_user and not github_user.user:
            github_user.user = User.objects.create(
                username=github_user.login,
                email=github_user.email,
            )
            github_user.save()
        return github_user.user
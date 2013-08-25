from django.contrib import admin, messages
from github.models import Application, User, Authentication, Repository, Key
from github.tasks import fetch_repo


class UserAdmin(admin.ModelAdmin):
    readonly_fields = User._meta.get_all_field_names()
    has_add_permission = lambda s, r: False
    has_delete_permission = lambda s, r, o = None: False

    actions = ['update_repos', 'update', 'update_keys']
    list_display = ('login', 'uid', 'email')

    def update_keys(self, request, queryset):
        for user in queryset.all():
            user.update_keys()

    def update_repos(self, request, queryset):
        for user in queryset.all():
            user.update_repositories()

    def update(self, request, queryset):
        for user in queryset.all():
            user.update_user()


class RepositoryAdmin(admin.ModelAdmin):
    readonly_fields = Repository._meta.get_all_field_names()
    has_add_permission = lambda s, r: False
    has_delete_permission = lambda s, r, o = None: False

    list_display = ('name',
                    'owner',
                    'forks',
                    'watchers',
                    'open_issues',
                    'size',
                    'language',
                    'homepage',
                    'created_at',
                    'updated_at')
    actions = ['refresh', 'fetch_repo']

    date_hierarchy = 'created_at'

    def fetch_repo(self, request, queryset):
        for repository in queryset.all():
            fetch_repo.delay(repository.pk)
            messages.info(request, "Fetching %s" % repository)

    def refresh(self, request, queryset):
        for repository in queryset.all():
            repository.refresh()


admin.site.register(Application,
                    list_display=('name',
                                  'client_id',
                                  'client_secret'))
admin.site.register(User, UserAdmin)
admin.site.register(Authentication,
                    readonly_fields=Authentication._meta.get_all_field_names(),
                    has_add_permission=lambda s, r: False,
                    has_delete_permission=lambda s, r, o=None: False,
                    list_display=('application',
                                  'redirect_uri',
                                  'scope'))

admin.site.register(Repository, RepositoryAdmin)
admin.site.register(Key, list_display=('title', 'user'),
                    readonly_fields=Key._meta.get_all_field_names(),
                    has_add_permission=lambda s, r: False,
                    has_delete_permission=lambda s, r, o=None: False)
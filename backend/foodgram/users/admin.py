from django.contrib import admin

from users.models import Subscribe, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email',
                    'first_name', 'last_name', )
    search_fields = ('username', 'first_name', 'last_name',)
    list_filter = ('is_superuser', 'is_staff', 'is_active', )
    empty_value_display = '-пусто-'


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author', )
    search_fields = ('author__username', 'author__email',
                     'user__username', 'user__email')
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Subscribe, SubscribeAdmin)

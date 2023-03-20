from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
	("Profile", {
			"fields": ("username","realname","phone","email","msg_agree","secret_key",),
			"classes": ("wide",),
		},
	),
	("Permissions",{
			"fields": (
				"is_active",
				"is_staff",
				"is_superuser",
				# "user_permissions",
			),
		},
	),
	("Important Dates", {
			"fields": ("password","last_login", "date_joined", "uuid"),
			"classes": ("collapse",),   #접었다폈다
		},
	),
)
    list_display = ("id","realname","username", "is_superuser","is_staff")
    list_filter = ("is_superuser", "realname","is_staff")
    search_fields = ("username","realname","phone","email","secret_key",)
    ordering = ("id",)
    # filter_horizontal = (
    #     "groups",
    #     "user_permissions",
    # )
	
    readonly_fields = ("date_joined", "last_login",)

from django.contrib import admin

from .models import Boards, Topics,Posts

admin.site.register(Boards)
admin.site.register(Topics)
admin.site.register(Posts)
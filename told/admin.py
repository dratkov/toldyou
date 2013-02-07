from django.contrib import admin
from models import *

admin.site.register(Post)
admin.site.register(ShortComment)
admin.site.register(Category)
admin.site.register(Mood)
admin.site.register(PostShortCommentsUser)
from django.contrib import admin

from social.models import Comment, Post

admin.site.register(Post)
admin.site.register(Comment)

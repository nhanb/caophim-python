from django.contrib import admin

from .models import Board, Post

admin.site.register(Post)
admin.site.register(Board)

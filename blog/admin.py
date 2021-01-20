from django.contrib import admin
from .models import Post, Comments, Maintanence

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','slug','author','publish','created','updated','status']
    prepopulated_fields= {'slug': ('title',)}
    list_filter = ('status',)
    search_fields = ('title',)
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status','-publish']


admin.site.register(Post,PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display=['post','name','email','comments','created','updated','active']
    list_filter = ('active','created',)
    search_fields=('name','email','comments','post',)

admin.site.register(Comments,CommentAdmin)

class MiddleWare(admin.ModelAdmin):
    list_display = ['under_maintanence','middle_ware_class','middle_ware_app']

admin.site.register(Maintanence,MiddleWare)
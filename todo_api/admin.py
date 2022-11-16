from django.contrib import admin
from todo_api.models import Todos, Snippets, Product, Brand

class TodoAdmin(admin.ModelAdmin):
    list_display = ('task', 'timestamp', 'completed', 'updated', 'user')
admin.site.register(Todos, TodoAdmin)

class SnippetAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'code')
admin.site.register(Snippets, SnippetAdmin)

class BrandAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'image')
admin.site.register(Brand, BrandAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "name",  "price")#, "brand","image", "stock_aval")
admin.site.register(Product, ProductAdmin)

from django.contrib import admin
from todo_api.models import Todos, Snippets, Product

class TodoAdmin(admin.ModelAdmin):
    list_display = ('task', 'timestamp', 'completed', 'updated', 'user')
admin.site.register(Todos, TodoAdmin)

class SnippetAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'code')
admin.site.register(Snippets, SnippetAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "name",  "price")#, "brand","image", "stock_aval")
admin.site.register(Product, ProductAdmin)

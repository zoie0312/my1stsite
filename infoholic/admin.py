from django.contrib import admin
from .models import Article, Category, Feed

class ArticleAdmin(admin.ModelAdmin):
    date_hierarchy = "fetched_at"
    fields = ("readed", "title", "slug", "content", "category", "source", "link", "reader")
    list_display = ["title", "category", "source", "reader", "readed",]
    list_display_links = ["title"]
    list_editable = ["readed", "reader"]
    list_filter = ["readed", "category", "source", "reader"]
    prepopulated_fields = {"slug": ("title", "link",)}
    search_fields = ["title", "content"]

class CategoryAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    fields = ("name", "slug_name", "owners")
    list_display = ["name", "updated_at"]
    list_display_links = ["name"]
    list_editable = []
    list_filter = ["updated_at", "owners"]
    prepopulated_fields = {"slug_name": ("name",)}
    search_fields = ["name"]

class FeedAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    fields = ("title", "slug", "link", "category", "owners")
    list_display = ["title", "category"]
    list_display_links = ["title"]
    list_editable = ["category"]
    list_filter = ["category", "owners"]
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ["title"]
                    

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Feed, FeedAdmin)

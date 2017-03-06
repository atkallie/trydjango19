from django.contrib import admin

from Posts.models import Post
# Register your models here.


class PostsModelAdmin(admin.ModelAdmin):
    #specify which fields you'd like to be displayed in the post row
    list_display = ["title","lastUpdated", "created", "image"]
    #specify which fields in your display you wish to be linked
    list_display_links = ["lastUpdated"]
    #specify which fields you'd like to be editable straight from the list view
    list_editable = ["title"]
    #add filters based on certain fields
    list_filter = ["lastUpdated","created"]
    #add fields that are searchable
    search_fields = ["title","content"]

    #Class reads metadata from model to provide model-centric admin interface admins can manage content on site
    #This class specifies the class to read metadata from
    class Meta:
        model = Post

admin.site.register(Post, PostsModelAdmin)
from django import forms
from Posts.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title","content","image","draft","publishDate"] #fields in model to be included in the form
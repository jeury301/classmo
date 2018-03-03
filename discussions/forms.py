from django import forms

class PostForm(forms.Form):
    title = forms.CharField(label='Title', max_length=280)
    body = forms.CharField(label='Text', max_length=3000, widget=forms.Textarea)

class CommentForm(forms.Form):
    body = forms.CharField(label='Text', max_length=3000, widget=forms.Textarea)
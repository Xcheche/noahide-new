from django import forms

from blog.models import Comment



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Comment'}),
            
        }
        # labels = {
        #     'name': 'Name',
        #     'content': 'Comment',
        # }
        # help_texts = {
        #     'name': 'Enter your name',
        #     'content': 'Enter your comment',
        # }
        # error_messages = {
        #     'name': {
        #         'required': 'Name is required',
        #         'max_length': 'Name is too long',
        #     },
        #     'content': {
        #         'required': 'Comment is required',
        #     },
        # }
from django import forms

from blog.models import Comment



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Comment', 'style': 'width: 100%;'}),
        }
        labels = {
            'name': 'Name',
            'content': 'Comment',
            
        }
        # help_texts = {
        #     'name': 'Enter your name',
        #     'content': 'Enter your comment',
        # }
        error_messages = {
            'name': {
                'required': 'Name is required',
                'max_length': 'Name is too long',
            },
            'content': {
                'required': 'Comment is required',
            },
        }
        
        
        
        def clean_name(self):
            name = self.cleaned_data.get('name')
            if not name:
                raise forms.ValidationError("Name is required")
            if Comment.objects.filter(name=name).exists():
                raise forms.ValidationError("Name already exists")
            if len(name) < 2:
                raise forms.ValidationError("Name is too short")
            return name
    
        def clean_content(self):
            content = self.cleaned_data.get('content')
            if not content:
                raise forms.ValidationError("Comment is required")
            return content
    
        def clean(self):
            cleaned_data = super().clean()
            name = cleaned_data.get('name')
            content = cleaned_data.get('content')
            if not name or not content:
                raise forms.ValidationError("Both fields are required")
            return cleaned_data
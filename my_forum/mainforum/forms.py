from django import forms
from .models import Topics

class TopicForm(forms.ModelForm):
    # message in from another model
    message=forms.CharField(widget=forms.Textarea(attrs={'row':'5', 'placeholder': 'whats on your mind?'}),

                            max_length=2000,
                            help_text="Write your message here. Max char is 2000. ")

    class Meta:
        model=Topics
        fields=['subject','message']
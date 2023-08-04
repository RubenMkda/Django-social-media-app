from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Posts

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class PotsForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['content', 'url_image']
        labels = {
            "content": "",
            "url_image": "Image url"
        }
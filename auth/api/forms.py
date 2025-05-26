from django import forms
from api.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        # hash the password properly
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user



class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


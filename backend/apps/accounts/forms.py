from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")

        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "w-full rounded-md px-3 bg-gray-100 placeholder:text-[13px] py-2 focus:outline-none focus:ring-1 focus:ring-blue-500"
            })

        self.fields['username'].widget.attrs['placeholder'] = 'Enter Username'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email address'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Tailwind styling for login fields
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "w-full rounded-md px-3 bg-gray-100 placeholder:text-[13px] py-2 focus:outline-none focus:ring-1 focus:ring-blue-500"
            })

        # Placeholders
        self.fields['username'].widget.attrs['placeholder'] = 'Enter Username'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter Password'
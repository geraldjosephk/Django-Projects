from dataclasses import fields
from pyexpat import model
from django import forms
from .models import Account, UserProfile


class RegistrationForm(forms.ModelForm):
    """Form model for registering user"""

    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Account
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "email",
            "password",
        ]

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password does not match!")

    def __init__(self, *args, **kwargs):
        # Enter placeholders in fields
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["placeholder"] = "Enter First Name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Enter Last Name"
        self.fields["email"].widget.attrs["placeholder"] = "johndoe@examplemail.com"
        self.fields["phone_number"].widget.attrs["placeholder"] = "Enter phone number"
        self.fields["password"].widget.attrs["placeholder"] = "Enter password"
        self.fields["confirm_password"].widget.attrs["placeholder"] = "Confirm password"

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("first_name", "last_name", "phone_number")

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        required=False,
        error_messages={"invalid": ("Image files only")},
        widget=forms.FileInput,
    )

    class Meta:
        model = UserProfile
        fields = (
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "country",
            "profile_picture",
        )

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

from django import forms
from django.utils.translation import gettext as _
from user.models import User

class UserCreationForm(forms.ModelForm): 
    password1 = forms.CharField(
        label=_('Password*'),
        widget=forms.PasswordInput(
            attrs={'placeholder': _('Password*')}
        )
    )
    password2 = forms.CharField(
        label=_('Password repeat*'),
        widget=forms.PasswordInput(
            attrs={'placeholder': _('Password repeat*')}
        )
    )
    login = forms.CharField(
        max_length=30,
        label=_('Login*'),
        widget=forms.TextInput(
            attrs={'placeholder': _('Login*')}
        ),
        required=False
    )
    firma = forms.CharField(
        max_length=30,
        label=_('Firma*'),
        widget=forms.TextInput(
            attrs={'placeholder': _('Firma*')}
        ),
        required=False
    )
    fname = forms.CharField(
        max_length=30,
        label=_('Fname*'),
        widget=forms.TextInput(
            attrs={'placeholder': _('Fname*')}
        ),
        required=False
    )
    lname = forms.CharField(
        max_length=30,
        label=_('Lname*'),
        widget=forms.TextInput(
            attrs={'placeholder': _('Lname*')}
        ),
        required=False
    )
    sname = forms.CharField(
        max_length=30,
        label=_('Sname*'),
        widget=forms.TextInput(
            attrs={'placeholder': _('Sname*')}
        ),
        required=False
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Email'),
                'autocomplete':'email'
            }),
        required=False
    )

    class Meta:
        model = User
        fields = ('email','password1','password2','fname','lname','sname','login','firma')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords do not match"))
        return password2

    def clean_name(self):
        name = self.cleaned_data.get('fname')
        if not name:
            name = User.generate_name()
        return name

    def save(self, *args, commit = True, **kwargs):
        user = super().save(*args, **kwargs)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user
    
class LogInForm(forms.Form): 
    login = forms.CharField(
        max_length=16,
        label=_('Login*:'),
        widget=forms.TextInput(
            attrs={'placeholder': _('Login')}
        ),
        required=True
    )
    password = forms.CharField(
        label=_('Password*:'),
        widget=forms.PasswordInput(
            attrs={'placeholder': _('Password'),'autocomplete':'password'}
        ),
        required=True
    )

    class Meta:
        fields = "__all__"
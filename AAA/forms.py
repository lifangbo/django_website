
from django import forms
from django.contrib.auth import password_validation
from .models import user_ext
import unicodedata
from django.utils.translation import ugettext, ugettext_lazy as _


class AAASetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    new_password = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(AAASetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password(self):
        password = self.cleaned_data.get('new_password')

        password_validation.validate_password(password, self.user)

        return password

    def save(self, commit=True):
        password = self.cleaned_data["new_password"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class AAAPasswordChangeForm(AAASetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = dict(AAASetPasswordForm.error_messages, **{
        'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
    })
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': ''}),
    )

    field_order = ['old_password', 'new_password']

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password


class AAAReadOnlyPasswordHashField(forms.Field):

    def bound_data(self, data, initial):
        # Always return initial because the widget doesn't
        # render an input field.
        return initial

    def has_changed(self, initial, data):
        return False

class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super(UsernameField, self).to_python(value))

class AAAUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given (username or phone_number) and
    password.
    """

    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        strip=False,
    )

    class Meta:
        model = user_ext
        fields = ("username", "phone_number", "is_staff", "is_active")
        field_classes = {'username': UsernameField}

    def clean_password(self):
        password = self.cleaned_data.get("password")
        self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(self.cleaned_data.get('password'), self.instance)

        return password

    def save(self, commit=True):
        user = super(AAAUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class AAAUserChangeForm(forms.ModelForm):

    class Meta:
        model = user_ext
        #fields = '__all__'
        exclude = ('is_superuser','date_joined', 'last_login', 'id', 'user_ptr_id', 'password', 'username')
        field_classes = {'username': UsernameField}



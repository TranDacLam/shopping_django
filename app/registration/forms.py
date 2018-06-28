from django import forms
from django.contrib.auth import login
from django.contrib.auth import get_user_model
import messages as msg

class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(), required=False)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if email and password:
            try:
                USER_MODEL = get_user_model()
                user = USER_MODEL.objects.get(email=email.strip())
            except USER_MODEL.DoesNotExist:
                raise forms.ValidationError(
                    msg.EMAIL_NOT_EXIST, code='invalid')

            if user:
                if not user.check_password(password):
                    raise forms.ValidationError(
                        msg.PASSWORD_WRONG, code='invalid')

                if user.is_active:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(self.request, user)
                else:
                    raise forms.ValidationError(msg.INACTIVE, code='invalid')
            else:
                raise forms.ValidationError(
                    msg.EMAIL_NOT_EXIST, code='invalid')
        else:
            raise forms.ValidationError(
                    msg.REQUIRED_E_P, code='invalid')

        return cleaned_data


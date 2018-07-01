from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from core.custom_models import User
from django.conf import settings
from django.utils import timezone
import datetime
import random
import sha
import mail
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


class RegisteForm(UserCreationForm):

    email = forms.CharField(widget=forms.TextInput())
    phone = forms.CharField(widget=forms.TextInput(), max_length=11, min_length=10)
    full_name = forms.CharField(widget=forms.TextInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(RegisteForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        exclude = ['is_staff', 'is_active', 'date_joined', 'modified',
                   'token_last_expired', 'activation_key', 'key_expires', 'password']


    def clean_email(self):
        cleaned_data = super(RegisteForm, self).clean()
        email = cleaned_data.get("email")

        USER_MODEL = get_user_model()
        user = USER_MODEL.objects.filter(email=email.strip())
        # Check user exist in system
        if len(user) > 0:
            if not user[0].is_active:
                raise forms.ValidationError(msg.INACTIVE, code='invalid')

        return email

    def clean_password2(self):
        cleaned_data = super(RegisteForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            self.add_error('password2', msg.PASSWORD_COMFIRM)

        return password2

    def create_activation_key(self, email):
        activation_key = None
        try:
            salt = sha.new(str(random.random())).hexdigest()[:5]
            activation_key = sha.new(salt + email).hexdigest()
            print "##### Current User Register : ", email
            print "##### Current Activation Key : ", activation_key
        except Exception, e:
            print 'Save Form Error ', e
            raise Exception('Internal Server Error.')
        return activation_key


    def send_activation_mail(self, full_name, email, activation_key):
        try:
            
            message_html = "registration/mail/account_created_confirm.html"
            message_txt = "registration/mail/account_created_confirm.txt"
            subject = _(
                "[Metiz] You've been created an account - Click to Verify!")

            protocol = 'http'
            if self.request.is_secure():
                protocol = 'https'
            logo_url = '/static/assets/websites/images/logofix.png'
            url_activate = self.request.build_absolute_uri(
                reverse('confirm-activation', kwargs={'activation_key': activation_key}))
            data_binding = {
                "protocol": protocol,
                'full_name': full_name,
                'email': email,
                'URL_LOGO': logo_url,
                'activate_url': url_activate,
                'site': str(Site.objects.get_current()),
                'HOT_LINE': settings.HOT_LINE
            }
            # Send email activation link
            mail.send_mail(subject, message_txt, message_html, settings.DEFAULT_FROM_EMAIL, [
                                  email], data_binding)

        except Exception, e:
            print 'Save Form Error ', e
            raise Exception('Internal Server Error.')

    def save(self):
        # call save function of super
        user = super(RegisteForm, self).save(commit=False)
        try:
            key_expires = timezone.now() + datetime.timedelta(settings.KEY_ACTIVATION_EXPIRES)
            user.activation_key = self.create_activation_key(user.email)
            user.key_expires = key_expires
            user.save()

            self.send_activation_mail(user.full_name, user.email, user.activation_key)

            return user

        except Exception, e:
            print 'Save Form Error ', e
            raise Exception('Internal Server Error.')


class ProfileForm(forms.Form):

    full_name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    birth_date = forms.DateField(required=False)
    address = forms.CharField(required=False)
    gender = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(ProfileForm, self).__init__(*args, **kwargs)

    def save(self):
        self.user.full_name = self.cleaned_data.get('full_name')
        self.user.phone = self.cleaned_data.get('phone')
        self.user.birth_date = self.cleaned_data.get('birth_date')
        self.user.address = self.cleaned_data.get('address')
        self.user.gender = self.cleaned_data.get('gender')
        self.user.save()
        return self.user


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(required=True)
    new_password = forms.CharField(required=True)
    new_password2 = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        valid = self.user.check_password(old_password)
        if not valid:
            self.add_error('old_password', _("The old password fields did not match."))
        return old_password

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        new_password = self.cleaned_data.get('new_password')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password != new_password2:
            self.add_error('new_password2', _("The old password fields did not match."))
        return cleaned_data

    def save(self, commit=True):
        """
        Saves the new password.
        """
        if commit:
            self.user.set_password(self.cleaned_data["new_password"])
            self.user.save()
        return self.user

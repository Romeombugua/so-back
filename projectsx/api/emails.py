from templated_mail.mail import BaseEmailMessage
from django.contrib.auth.tokens import default_token_generator
from djoser import utils
from djoser.conf import settings
from .constants import ReactUrl, SiteName

class ActivationEmail(BaseEmailMessage):
    template_name = "email/activation.html"

    def get_context_data(self):
        # ActivationEmail can be deleted
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.ACTIVATION_URL.format(**context)
        context["domain"] = ReactUrl.REACT_URL # Your site domain
        context["protocol"] = "https" # Your site protocol e.g. ("http", "https")
        context["site_name"] = SiteName.SITE_NAME
        return context
    
class PasswordResetEmail(BaseEmailMessage):
    template_name = "email/password_reset.html"

    def get_context_data(self):
        # PasswordResetEmail can be deleted
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.PASSWORD_RESET_CONFIRM_URL.format(**context)
        context["domain"] = ReactUrl.REACT_URL # Your site domain
        context["protocol"] = "https"
        context["site_name"] = SiteName.SITE_NAME # Your site protocol e.g. ("http", "https")
        return context
    
class PasswordChangedConfirmationEmail(BaseEmailMessage):
    template_name = "email/password_changed_confirmation.html"

    def get_context_data(self):
        # PasswordResetEmail can be deleted
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.PASSWORD_RESET_CONFIRM_URL.format(**context)
        context["domain"] = ReactUrl.REACT_URL # Your site domain
        context["protocol"] = "https"
        context["site_name"] = SiteName.SITE_NAME # Your site protocol e.g. ("http", "https")
        return context
    
class ConfirmationEmail(BaseEmailMessage):
    template_name = "email/confirmation.html"

    def get_context_data(self):
        # PasswordResetEmail can be deleted
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["domain"] = ReactUrl.REACT_URL # Your site domain
        context["protocol"] = "https"
        context["site_name"] = SiteName.SITE_NAME # Your site protocol e.g. ("http", "https")
        return context
from django.conf import settings
from django.middleware.locale import LocaleMiddleware
from django.utils.translation import get_language, get_language_from_path
from django.utils import translation


class SetDefaultLocaleMiddleware(LocaleMiddleware):

    def process_request(self, request):
        lang_code = (get_language_from_path(request.path_info) or
                     settings.LANGUAGE_CODE)

        translation.activate(lang_code)
        request.LANGUAGE_CODE = translation.get_language()
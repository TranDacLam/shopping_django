from django.utils.deprecation import MiddlewareMixin
from models import Category  


class GetCategoryMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.categories = Category.objects.all()

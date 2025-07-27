from django.urls import path
from . import views

urlpatterns = [
    path('admin/get-category-attributes/<int:category_id>/', get_category_attributes, name='get_category_attributes'),
]

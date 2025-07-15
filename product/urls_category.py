from django.urls import path
from product import views


urlpatterns = [
    path("", views.ViewCategory.as_view(), name="category-list"),
    path("<int:id>/", views.ViewSpecificCategory.as_view(), name="specific-category"),
]

from django.urls import path
from product import views


urlpatterns = [
    # path("", views.ViewCategory.as_view(), name="category-list"),
    path("", views.CategoryList.as_view(), name="category-list"),
    # path("<int:id>/", views.ViewSpecificCategory.as_view(), name="specific-category"),
    path("<int:id>/", views.CategoryDetails.as_view(), name="specific-category"),
]

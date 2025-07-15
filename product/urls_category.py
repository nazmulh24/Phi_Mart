from django.urls import path
from product import views


urlpatterns = [
    # path("", views.view_categories, name="category-list"),
    path("", views.ViewCategory.as_view(), name="category-list"),
    # path("<int:pk>/", views.view_specific_category, name="specific-category"),
    path("<int:pk>/", views.ViewSpecificCategory.as_view(), name="specific-category"),
]

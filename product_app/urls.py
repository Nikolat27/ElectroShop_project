from . import views
from django.urls import path

app_name = "product_app"
urlpatterns = [
    path("detail/<int:pk>", views.product_detail, name="product_detail"),
    path("add_comment/<int:pk>", views.add_comment, name="add_comment"),
    path("store", views.store_page, name="store_page"),
    path('filter-data', views.filter_data, name="filter-data"),
    path('clear-filters', views.clear_filters, name="clear_filters"),
    path('add_like/<int:pk>', views.add_like, name="add_like"),
    path('wishlists', views.wishlist_page, name="wishlist_page"),
    path("autocomplete", views.autocomplete, name="autocomplete"),
    path("filter_colors/<int:pk>/", views.filter_color_quantities, name="filter_colors"),
    path("x", views.x),
]

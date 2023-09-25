from . import views
from django.urls import path

app_name = "products_app"
urlpatterns = [
    path("<str:slug>", views.product_detail, name="detail"),
    path("<str:cat>", views.product_detail, name="detail"),
    path("store/", views.store_page, name="store_page"),
    path("search/", views.search_page, name="search_page"),
    path("like/<slug:slug>/<int:pk>", views.like, name="like"),
    path("autocomplete/", views.autocomplete, name="autocomplete"),
    path("ajax-add-review/<int:pk>", views.ajax_add_review, name="ajax_add_review"),
    path("filter_products/", views.filter_products, name="filter_products"),
    path("wishlist_products/", views.wishlist, name="wishlists_products"),
    path("remove_wishlist/<int:pk>", views.remove_wishlist, name="remove_wishlists_products"),
    path("contact_us/", views.contact_us, name="contact_us"),
]

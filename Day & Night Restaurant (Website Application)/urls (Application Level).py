from . import views
from django.urls import path
from django.conf import settings
from django.views.static import serve
from django.urls import re_path



urlpatterns = [
    path("", views.homepage, name = "homepage"),
    path("homepage/", views.homepage, name = "homepage"),
    path("about_page/", views.about_page, name = "about_page"),

    path("appetizers/", views.Appetizers, name = "appetizers"),
    path("appetizers/<int:item_id>", views.Appetizer_detail, name = "appetizers_detail"),

    path("entrees/", views.entrees, name = "entrees"),
    path("entrees/<int:item_id>/", views.entrees_detail, name = "entrees_detail"),

    path("drinks/", views.drinks, name = "drinks"),
    path("drinks/<int:item_id>/", views.drink_detail, name = "drink_detail"),

    path("desserts/", views.desserts, name = "desserts"),
    path("desserts/<int:item_id>", views.desserts_detail, name = "desserts_detail"),

    path("reservation/", views.reservation, name ="reservation"),
    path("reservation_success/", views.reservation_success, name = "reservation_success"),

    path("take_out/", views.take_out, name = "take_out"),
    path("checkout_screen/", views.checkout_screen, name = "checkout_screen"),
    path("checkout_success/<int:order_id>/", views.checkout_success, name = "checkout_success"),

    path("signup_page/", views.signup_page, name = "signup_page"),


    path("cart_view/", views.cart_view, name = "cart_view" ),
    path("add_to_cart/<str:item_type>/<int:item_id>/", views.add_to_cart, name = "add_to_cart"),
    path("increase_cart_quantity_button/<str:item_type>/<int:item_id>/", views.increase_cart_quantity_button, name="increase_cart_quantity_button"),
    path("decrease_cart_quantity_button/<str:item_type>/<int:item_id>/", views.decrease_cart_quantity_button, name="decrease_cart_quantity_button"),
    path("clear_cart/", views.clear_cart, name = "clear_cart"),

    path("order_history/", views.order_history, name="order_history"),
    path("reorder/<int:order_id>/", views.reorder_function, name = "reorder_function"),


    path("api/reservations/", views.reservations_api, name = "reservations_api"),

    ]
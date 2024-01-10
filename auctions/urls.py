from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("new", views.create_listing, name="create_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("view_watchlist", views.view_watchlist, name="view_watchlist"),
    path("view_categories", views.view_categories, name="view_categories"),
    path("categoty_details/<int:category_id>", views.category_details, name="category_details")
]

"""test_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include 

from . import views

app_name = "homepage"

urlpatterns = [
	path("",views.homepage, name="homepage"), # Path to the url create account
	path("addToCart/?=id<int:item>", views.add_to_cart,name="add_to_cart"), # <indicates> pos argument
	path("orders/", views.order_page, name="orders"),
    path("search/",views.search_page, name="search"),
    path("query", views.search, name="search_query"),
    path("submitOrder/", views.submit_order, name="submit_order"),
    path("remove_from_cart/?=id<int:item>", views.remove_from_cart, name="remove_from_cart"),
    path("cart", views.cart, name="cart"),
    path("retrieveOrder/", views.retrieve_order, name="retrieve_order"),
]

from django.urls import path

from records import views

app_name = 'records'
urlpatterns = [
    path("products/", views.ProductsView.as_view(), name="product_list"),
    path("user/register/", views.RegisterUser.as_view(), name="user-register"),
    path("user/login/", views.LoginUser.as_view(), name="user-login"),
    path("checkout/", views.SaveOrders.as_view(), name="order")
]

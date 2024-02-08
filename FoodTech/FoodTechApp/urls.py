from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path('Admin.html', views.Admin, name="Admin"), 
	       path('Login.html', views.Login, name="Login"), 
	       path('Register.html', views.Register, name="Register"),
	       path('Signup', views.Signup, name="Signup"),
	       path('UserLogin', views.UserLogin, name="UserLogin"),
	       path('AdminLogin', views.AdminLogin, name="AdminLogin"),
	       path('AddFood.html', views.AddFood, name="AddFood"), 
	       path('AddFoodAction', views.AddFoodAction, name="AddFoodAction"),
	       path('ViewOrders', views.ViewOrders, name="ViewOrders"),
	       path('Deliver', views.Deliver, name="Deliver"),
	       path('BrowseProducts.html', views.BrowseProducts, name="BrowseProducts"),
	       path('SearchProductAction', views.SearchProductAction, name="SearchProductAction"),
	       path('BookOrder', views.BookOrder, name="BookOrder"),
]
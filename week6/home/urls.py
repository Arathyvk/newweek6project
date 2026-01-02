from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [ 
     path('admin/', admin.site.urls),
    path('homes', views.homes, name="homes"),
    path('',views.login_view, name='login_view'),
    path('signup/',views.signup_view, name='signup_view'),
    path('logout/',views.logout_view, name='logout_view'),
    path('newadmin/', include('newadmin.urls')),
]    




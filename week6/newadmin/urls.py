from django.urls import path
from . import views

urlpatterns = [
    path("", views.admin_login, name="admin_login"), 
    path("admin-create/", views.create_admin, name="create_admin"),
    path("admin-edit/<int:id>/", views.edit_admin, name="edit_admin"),
    path("admin-delete/<int:id>/", views.delete_admin, name="delete_admin"),
    path("admin-users/", views.user_list, name="user_list"),
]

# attendance/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("visit/<int:org_id>/", views.confirm_org, name="confirm_org"),
    path("visit/<int:org_id>/details/", views.enter_details, name="enter_details"),
    path("success/<int:visitor_id>/", views.success, name="success"),
    path("jadmin/organisations/", views.admin_org_list, name="admin_org_list"),
]

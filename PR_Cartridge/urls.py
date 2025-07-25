
from . import views ;  from django.urls import path
urlpatterns = [
    path("", views.user_login, name="user_login"),
    path("login/", views.login_view, name="login_view"),
    path("new-request/", views.cartridge_request_create, name='cartridge_request_create'),
    path("cartridge-requests/", views.cartridge_request_list, name='cartridge_request_list'),
    path("cancel-request/<int:sl_no>/", views.cancel_request, name="cancel_request"),
    path('approve/', views.approve_requests, name='approve_requests'),
    path('approve/<int:pk>/', views.approve_single_request, name='approve_single_request'),
    path('issue/', views.issue_requests, name='issue_requests'),
    path('issue/<int:pk>/', views.issue_single_request, name='issue_single_request'),
    path('get-hod-name/', views.get_hod_name_by_printer, name='get_hod_name_by_printer'),
    path('report/',views.report_all_list, name='report_all'),path('logout/', views.logout_view, name='logout_view'),
    path("validate-printer-no/", views.validate_printer_no, name="validate_printer_no"),
    path("get-printer-details/", views.get_printer_details, name="get_printer_details"),
]

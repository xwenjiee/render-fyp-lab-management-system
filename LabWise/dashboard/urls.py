from django.urls import path
from . import views

urlpatterns = [
    path("index/", views.index, name="dashboard-index"),
    path("items/", views.items, name="dashboard-items"),
    path(
        "items/delete/<int:pk>/",
        views.item_delete,
        name="dashboard-items-delete",
    ),
    path("items/edit/<int:pk>/", views.item_edit, name="dashboard-items-edit"),
    path("categories/", views.categories, name="dashboard-categories"),
    path(
        "categories/delete/<int:pk>/",
        views.category_delete,
        name="dashboard-categories-delete",
    ),
    path(
        "categories/edit/<int:pk>/",
        views.category_edit,
        name="dashboard-categories-edit",
    ),
    path("customers/", views.customers, name="dashboard-customers"),
    path(
        "customers/delete/<int:pk>/",
        views.account_delete,
        name="dashboard-account-delete-customer",
    ),
    path("staff/", views.staff, name="dashboard-staff"),
    path(
        "staff/delete/<int:pk>/",
        views.account_deleteStaff,
        name="dashboard-account-delete",
    ),
    path("booking/", views.booking, name="dashboard-booking"),
    path(
        "booking/approve/<int:pk>/",
        views.booking_approve,
        name="dashboard-booking-approve",
    ),
    path(
        "booking/complete/<int:pk>/",
        views.booking_complete,
        name="dashboard-booking-complete",
    ),
    path(
        "booking/reject/<int:pk>/",
        views.booking_reject,
        name="dashboard-booking-reject",
    ),
    path(
        "booking/delete/<int:pk>/",
        views.booking_deleteRecord,
        name="dashboard-booking-deleteRecord",
    ),
    path("serviceItem/", views.serviceItem, name="dashboard-serviceItem"),
    path(
        "serviceItem/delete/<int:pk>/",
        views.serviceItem_delete,
        name="dashboard-serviceItem-delete",
    ),
    path(
        "serviceItem/edit/<int:pk>/",
        views.serviceItem_edit,
        name="dashboard-serviceItem-edit",
    ),
    path("service/", views.service, name="dashboard-service"),
    path(
        "service/delete/<int:pk>/",
        views.service_delete,
        name="dashboard-service-delete",
    ),
    path(
        "service/edit/<int:pk>/",
        views.service_edit,
        name="dashboard-service-edit",
    ),
    path(
        "catalogue/",
        views.guest_view,
        name="guest-view",
    ),
]

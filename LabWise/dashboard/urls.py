from django.urls import path
from . import views

urlpatterns = [
    path("index/", views.index, name="dashboard-index"),
    path("items/", views.products, name="dashboard-products"),
    path(
        "items/delete/<int:pk>/",
        views.product_delete,
        name="dashboard-products-delete",
    ),
    path(
        "items/detail/<int:pk>/",
        views.product_detail,
        name="dashboard-products-detail",
    ),
    path("items/edit/<int:pk>/", views.product_edit, name="dashboard-products-edit"),
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
    path("staff/", views.staff, name="dashboard-staff"),
    path(
        "customers/detail/<int:pk>/",
        views.customer_detail,
        name="dashboard-customer-detail",
    ),
    path("order/", views.order, name="dashboard-order"),
    path(
        "order/approve/<int:pk>/",
        views.order_approve,
        name="dashboard-order-approve",
    ),
    path(
        "order/complete/<int:pk>/",
        views.order_complete,
        name="dashboard-order-complete",
    ),
    path(
        "order/reject/<int:pk>/",
        views.order_reject,
        name="dashboard-order-reject",
    ),
    path(
        "order/delete/<int:pk>/",
        views.order_deleteRecord,
        name="dashboard-order-deleteRecord",
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

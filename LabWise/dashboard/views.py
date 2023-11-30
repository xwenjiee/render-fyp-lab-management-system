from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import (
    Item,
    Booking,
    Category,
    Service,
    ServiceItem,
)
from .forms import (
    ProductForm,
    StaffForm,
    CategoryForm,
    ServiceForm,
    ServiceItemForm,
    ServiceBookingForm,
    ServiceItemEditForm,
    ProductEditForm,
    ServiceEditForm,
    CategoryEditForm,
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import auth_users, allowed_users

# Create your views here.


@login_required(login_url="user-login")
def index(request):
    staff = User.objects.filter(is_staff=True)
    staff_count = staff.count()
    product = Item.objects.all()
    product_count = product.count()
    order = Booking.objects.all()
    order_count = order.count()
    customer = User.objects.filter(is_staff=False)
    customer_count = customer.count()
    category = Category.objects.all()
    category_count = category.count()
    service = Service.objects.all()
    service_count = service.count()
    serviceItem = ServiceItem.objects.all()
    serviceItem_count = serviceItem.count()

    if request.method == "POST":
        form2 = ServiceBookingForm(request.POST)

        if form2.is_valid():
            obj = form2.save()
            obj.customer = request.user

            obj.save()
            return redirect("dashboard-index")

    else:
        form2 = ServiceBookingForm()
    context = {
        "form2": form2,
        "order": order,
        "staff": staff,
        "staff_count": staff_count,
        "product": product,
        "product_count": product_count,
        "order_count": order_count,
        "customer_count": customer_count,
        "category": category,
        "category_count": category_count,
        "service": service,
        "service_count": service_count,
        "serviceItem": serviceItem,
        "serviceItem_count": serviceItem_count,
    }
    return render(request, "dashboard/index.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=[True])
def products(request):
    staff = User.objects.filter(is_staff=True)
    staff_count = staff.count()
    product = Item.objects.all()
    product_count = product.count()
    customer = User.objects.filter(is_staff=False)
    customer_count = customer.count()
    order = Booking.objects.all()
    order_count = order.count()
    category = Category.objects.all()
    category_count = category.count()
    service = Service.objects.all()
    service_count = service.count()
    serviceItem = ServiceItem.objects.all()
    serviceItem_count = serviceItem.count()
    product_quantity = Item.objects.filter(name="")
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get("name")
            messages.success(request, f"{product_name} has been added")
            return redirect("dashboard-products")
    else:
        form = ProductForm()
    context = {
        "product": product,
        "form": form,
        "staff": staff,
        "staff_count": staff_count,
        "customer_count": customer_count,
        "product_count": product_count,
        "order_count": order_count,
        "category": category,
        "category_count": category_count,
        "service": service,
        "service_count": service_count,
        "serviceItem": serviceItem,
        "serviceItem_count": serviceItem_count,
    }
    return render(request, "dashboard/products.html", context)


# CATEGORY
@login_required(login_url="user-login")
@allowed_users(allowed_roles=[True])
def categories(request):
    staff = User.objects.filter(is_staff=True)
    staff_count = staff.count()
    product = Item.objects.all()
    product_count = product.count()
    customer = User.objects.filter(is_staff=False)
    customer_count = customer.count()
    order = Booking.objects.all()
    order_count = order.count()
    category = Category.objects.all()
    category_count = category.count()
    service = Service.objects.all()
    service_count = service.count()
    serviceItem = ServiceItem.objects.all()
    serviceItem_count = serviceItem.count()
    product_quantity = Item.objects.filter(name="")
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get("name")
            messages.success(request, f"{product_name} has been added")
            return redirect("dashboard-categories")
    else:
        form = CategoryForm()
    context = {
        "product": product,
        "form": form,
        "staff": staff,
        "staff_count": staff_count,
        "customer_count": customer_count,
        "product_count": product_count,
        "order_count": order_count,
        "category": category,
        "category_count": category_count,
        "service": service,
        "service_count": service_count,
        "serviceItem": serviceItem,
        "serviceItem_count": serviceItem_count,
    }
    return render(request, "dashboard/categories.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=[True])
def category_edit(request, pk):
    item = Category.objects.get(id=pk)
    if request.method == "POST":
        form = CategoryEditForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("dashboard-categories")
    else:
        form = CategoryEditForm(instance=item)
    context = {
        "form": form,
    }
    return render(request, "dashboard/categories_edit.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=[True])
def category_delete(request, pk):
    item = Category.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        return redirect("dashboard-categories")
    context = {"item": item}
    return render(request, "dashboard/categories_delete.html", context)


@login_required(login_url="user-login")
def product_detail(request, pk):
    context = {}
    return render(request, "dashboard/products_detail.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=[True])
def customers(request):
    staff = User.objects.filter(is_staff=True)
    staff_count = staff.count()
    customer = User.objects.filter(is_staff=False)
    customer_count = customer.count()
    product = Item.objects.all()
    product_count = product.count()
    order = Booking.objects.all()
    order_count = order.count()
    category = Category.objects.all()
    category_count = category.count()
    service = Service.objects.all()
    service_count = service.count()
    serviceItem = ServiceItem.objects.all()
    serviceItem_count = serviceItem.count()
    context = {
        "staff": staff,
        "staff_count": staff_count,
        "customer": customer,
        "customer_count": customer_count,
        "product_count": product_count,
        "order_count": order_count,
        "category": category,
        "category_count": category_count,
        "service": service,
        "service_count": service_count,
        "serviceItem": serviceItem,
        "serviceItem_count": serviceItem_count,
    }
    return render(request, "dashboard/customers.html", context)


@login_required(login_url="user-login")
# @allowed_users(allowed_roles=["Admin"])
@allowed_users(allowed_roles=[True])
def staff(request):
    staff = User.objects.filter(is_staff=True)
    staff_count = staff.count()
    customer = User.objects.filter(is_staff=False)
    customer_count = customer.count()
    product = Item.objects.all()
    product_count = product.count()
    order = Booking.objects.all()
    order_count = order.count()
    category = Category.objects.all()
    category_count = category.count()
    service = Service.objects.all()
    service_count = service.count()
    serviceItem = ServiceItem.objects.all()
    serviceItem_count = serviceItem.count()
    if request.method == "POST":
        form = StaffForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password1"),
                first_name=form.cleaned_data.get("first_name"),
                last_name=form.cleaned_data.get("last_name"),
                email=form.cleaned_data.get("email"),
                is_staff=True,
            )
            staff_name = form.cleaned_data.get("username")
            messages.success(request, f"{staff_name} has been added")
            return redirect("dashboard-staff")
    else:
        form = StaffForm()
    context = {
        "staff": staff,
        "form": form,
        "staff_count": staff_count,
        "customer": customer,
        "customer_count": customer_count,
        "product_count": product_count,
        "order_count": order_count,
        "category": category,
        "category_count": category_count,
        "service": service,
        "service_count": service_count,
        "serviceItem": serviceItem,
        "serviceItem_count": serviceItem_count,
    }
    return render(request, "dashboard/staff.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=[True])
def customer_detail(request, pk):
    staff = User.objects.filter(is_staff=True)
    staff_count = staff.count()
    customer = User.objects.filter(is_staff=False)
    customer_count = customer.count()
    product = Item.objects.all()
    product_count = product.count()
    order = Booking.objects.all()
    order_count = order.count()
    customers = User.objects.get(id=pk)
    category = Category.objects.all()
    category_count = category.count()
    service = Service.objects.all()
    service_count = service.count()
    serviceItem = ServiceItem.objects.all()
    serviceItem_count = serviceItem.count()
    context = {
        "staff": staff,
        "staff_count": staff_count,
        "customers": customers,
        "customer_count": customer_count,
        "product_count": product_count,
        "order_count": order_count,
        "category": category,
        "category_count": category_count,
        "service": service,
        "service_count": service_count,
        "serviceItem": serviceItem,
        "serviceItem_count": serviceItem_count,
    }
    return render(request, "dashboard/customers_detail.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=[True])
def product_edit(request, pk):
    item = Item.objects.get(id=pk)
    if request.method == "POST":
        form = ProductEditForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("dashboard-products")
    else:
        form = ProductEditForm(instance=item)
    context = {
        "form": form,
    }
    return render(request, "dashboard/products_edit.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=[True])
def product_delete(request, pk):
    item = Item.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        return redirect("dashboard-products")
    context = {"item": item}
    return render(request, "dashboard/products_delete.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=[True])
def order(request):
    staff = User.objects.filter(is_staff=True)
    staff_count = staff.count()
    order = Booking.objects.all()
    order_count = order.count()
    customer = User.objects.filter(is_staff=False)
    customer_count = customer.count()
    product = Item.objects.all()
    product_count = product.count()

    category = Category.objects.all()
    category_count = category.count()
    service = Service.objects.all()
    service_count = service.count()
    serviceItem = ServiceItem.objects.all()
    serviceItem_count = serviceItem.count()

    context = {
        "staff": staff,
        "staff_count": staff_count,
        "order": order,
        "customer_count": customer_count,
        "product_count": product_count,
        "order_count": order_count,
        "category": category,
        "category_count": category_count,
        "service": service,
        "service_count": service_count,
        "serviceItem": serviceItem,
        "serviceItem_count": serviceItem_count,
    }
    return render(request, "dashboard/order.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=[True])
def order_reject(request, pk):
    item = Booking.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        return redirect("dashboard-order")
    context = {"item": item}
    return render(request, "dashboard/order_reject.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=[True])
def order_deleteRecord(request, pk):
    item = Booking.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        return redirect("dashboard-order")
    context = {"item": item}
    return render(request, "dashboard/order_deleteRecord.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=[True])
def order_approve(request, pk):
    booking = Booking.objects.get(id=pk)
    # booking.item = Booking.objects.get(id=pk)
    if request.method == "POST":
        if booking.item:
            booking.item.status = "Occupied"
            booking.item.save()

        booking.bookingStatus = "Approved"
        booking.save()
        return redirect("dashboard-order")
    context = {"item": booking}
    return render(request, "dashboard/order_approve.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=[True])
def order_complete(request, pk):
    booking = Booking.objects.get(id=pk)
    # booking.item = Booking.objects.get(id=pk)
    if request.method == "POST":
        if booking.item:
            booking.item.status = "Available"
            booking.item.save()

        booking.bookingStatus = "Completed"
        booking.save()
        return redirect("dashboard-order")
    context = {"booking": booking}
    return render(request, "dashboard/complete_booking.html", context)


# service
@login_required(login_url="user-login")
@allowed_users(allowed_roles=[True])
def service(request):
    staff = User.objects.filter(is_staff=True)
    staff_count = staff.count()
    product = Item.objects.all()
    product_count = product.count()
    customer = User.objects.filter(is_staff=False)
    customer_count = customer.count()
    order = Booking.objects.all()
    order_count = order.count()
    category = Category.objects.all()
    category_count = category.count()
    service = Service.objects.all()
    service_count = service.count()
    serviceItem = ServiceItem.objects.all()
    serviceItem_count = serviceItem.count()
    product_quantity = Item.objects.filter(name="")
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get("name")
            messages.success(request, f"{product_name} has been added")
            return redirect("dashboard-service")
    else:
        form = ServiceForm()
    context = {
        "product": product,
        "form": form,
        "staff": staff,
        "category": category,
        "staff_count": staff_count,
        "customer_count": customer_count,
        "product_count": product_count,
        "order_count": order_count,
        "category_count": category_count,
        "service": service,
        "service_count": service_count,
        "serviceItem": serviceItem,
        "serviceItem_count": serviceItem_count,
    }
    return render(request, "dashboard/service.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=[True])
def service_edit(request, pk):
    item = Service.objects.get(id=pk)
    if request.method == "POST":
        form = ServiceEditForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("dashboard-service")
    else:
        form = ServiceEditForm(instance=item)
    context = {
        "form": form,
    }
    return render(request, "dashboard/service_edit.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=[True])
def service_delete(request, pk):
    item = Service.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        return redirect("dashboard-service")
    context = {"item": item}
    return render(request, "dashboard/service_delete.html", context)


# serviceitem
@login_required(login_url="user-login")
@allowed_users(allowed_roles=[True])
def serviceItem(request):
    staff = User.objects.filter(is_staff=True)
    staff_count = staff.count()
    product = Item.objects.all()
    product_count = product.count()
    customer = User.objects.filter(is_staff=False)
    customer_count = customer.count()
    order = Booking.objects.all()
    order_count = order.count()
    category = Category.objects.all()
    category_count = category.count()
    service = Service.objects.all()
    service_count = service.count()
    serviceItem = ServiceItem.objects.all()
    serviceItem_count = serviceItem.count()
    product_quantity = Item.objects.filter(name="")
    if request.method == "POST":
        form = ServiceItemForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get("name")
            messages.success(request, f"{product_name} has been added")
            return redirect("dashboard-serviceItem")
    else:
        form = ServiceItemForm()
    context = {
        "product": product,
        "form": form,
        "staff": staff,
        "category": category,
        "staff_count": staff_count,
        "customer_count": customer_count,
        "product_count": product_count,
        "order_count": order_count,
        "category_count": category_count,
        "service": service,
        "service_count": service_count,
        "serviceItem": serviceItem,
        "serviceItem_count": serviceItem_count,
    }
    return render(request, "dashboard/serviceItem.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=[True])
def serviceItem_edit(request, pk):
    item = ServiceItem.objects.get(id=pk)
    if request.method == "POST":
        form = ServiceItemEditForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("dashboard-serviceItem")
    else:
        form = ServiceItemEditForm(instance=item)
    context = {
        "form": form,
    }
    return render(request, "dashboard/serviceItem_edit.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=[True])
def serviceItem_delete(request, pk):
    item = ServiceItem.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        return redirect("dashboard-serviceItem")
    context = {"item": item, "serialNumber": item.serialNumber}
    return render(request, "dashboard/serviceItem_delete.html", context)


def guest_view(request):
    service = Service.objects.all()
    serviceItem = ServiceItem.objects.all()
    bookings = Booking.objects.filter(bookingStatus="Pending Approval")
    first = (
        ServiceItem.objects.all()
        .filter(status="Available")
        .distinct("name")
        .filter(booking__isnull=True)
    )
    second = (
        ServiceItem.objects.all()
        .filter(status="Available")
        .distinct("name")
        .exclude(booking__in=bookings)
    )

    final = first | second
    context = {
        "service": service,
        "serviceItem": final,
    }

    return render(request, "guest_view.html", context)

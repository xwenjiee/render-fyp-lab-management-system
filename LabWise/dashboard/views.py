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
from .decorators import auth_users, allowed_users, superuseronly

from django.db.models.query import QuerySet

# Create your views here.


@login_required(login_url="user-login")
def index(request):
    staff = User.objects.filter(is_staff=True)
    staff_count = staff.count()
    item = Item.objects.all()
    item_count = item.count()
    booking = Booking.objects.all()
    booking_count = booking.count()
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

            def extract_integer_from_queryset(queryset):
                if not isinstance(queryset, QuerySet):
                    raise ValueError("Input must be a Django QuerySet")

                # Check if the QuerySet has any items
                if queryset.exists():
                    # Assuming 'id' is the key you want to extract
                    first_item = queryset.first()
                    extracted_id = first_item.get(
                        "id"
                    )  # Change 'id' to the actual key in your data
                    if extracted_id is not None:
                        return int(extracted_id)
                    else:
                        raise ValueError("Key 'id' not found in the queryset item")
                else:
                    raise ValueError("QuerySet is empty")

            # Example usage:
            identity = User.objects.filter(username=request.user).values("id")
            result_integer = extract_integer_from_queryset(identity)

            print(result_integer)

            count = (
                Booking.objects.all()
                .filter(customer_id=result_integer)
                .filter(service=form2.cleaned_data.get("service"))
                .filter(bookingStatus="Active")
                .count()
            ) + (
                Booking.objects.all()
                .filter(customer_id=result_integer)
                .filter(service=form2.cleaned_data.get("service"))
                .filter(bookingStatus="Pending Approval")
                .count()
            )
            print(count)

            if count < 3:
                obj = form2.save()
                obj.customer = request.user
                obj.save()
                service = form2.cleaned_data.get("service")
                item = form2.cleaned_data.get("item")
                if service:
                    messages.success(request, f"{service} has been requested.")

                elif item:
                    messages.success(request, f"{item} has been requested.")

            else:
                service = form2.cleaned_data.get("service")
                messages.error(
                    request, f"{service} is requested/active for more than 3 slots."
                )

            return redirect("dashboard-index")

    else:
        form2 = ServiceBookingForm()
    context = {
        "form2": form2,
        "booking": booking,
        "staff": staff,
        "staff_count": staff_count,
        "item": item,
        "item_count": item_count,
        "booking_count": booking_count,
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
def items(request):
    staff = User.objects.filter(is_staff=True)
    staff_count = staff.count()
    item = Item.objects.all()
    item_count = item.count()
    customer = User.objects.filter(is_staff=False)
    customer_count = customer.count()
    booking = Booking.objects.all()
    booking_count = booking.count()
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
            return redirect("dashboard-items")
    else:
        form = ProductForm()
    context = {
        "item": item,
        "form": form,
        "staff": staff,
        "staff_count": staff_count,
        "customer_count": customer_count,
        "item_count": item_count,
        "booking_count": booking_count,
        "category": category,
        "category_count": category_count,
        "service": service,
        "service_count": service_count,
        "serviceItem": serviceItem,
        "serviceItem_count": serviceItem_count,
    }
    return render(request, "dashboard/item.html", context)


# CATEGORY
@login_required(login_url="user-login")
@allowed_users(allowed_roles=[True])
def categories(request):
    staff = User.objects.filter(is_staff=True)
    staff_count = staff.count()
    item = Item.objects.all()
    item_count = item.count()
    customer = User.objects.filter(is_staff=False)
    customer_count = customer.count()
    booking = Booking.objects.all()
    booking_count = booking.count()
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
        "item": item,
        "form": form,
        "staff": staff,
        "staff_count": staff_count,
        "customer_count": customer_count,
        "item_count": item_count,
        "booking_count": booking_count,
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
@allowed_users(allowed_roles=[True])
def customers(request):
    staff = User.objects.filter(is_staff=True)
    staff_count = staff.count()
    customer = User.objects.filter(is_staff=False)
    customer_count = customer.count()
    item = Item.objects.all()
    item_count = item.count()
    booking = Booking.objects.all()
    booking_count = booking.count()
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
        "item_count": item_count,
        "booking_count": booking_count,
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
    item = Item.objects.all()
    item_count = item.count()
    booking = Booking.objects.all()
    booking_count = booking.count()
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
        "item_count": item_count,
        "booking_count": booking_count,
        "category": category,
        "category_count": category_count,
        "service": service,
        "service_count": service_count,
        "serviceItem": serviceItem,
        "serviceItem_count": serviceItem_count,
    }
    return render(request, "dashboard/staff.html", context)


@login_required(login_url="user-login")
# @allowed_users(allowed_roles=["Admin"])


@allowed_users(allowed_roles=[True])
@superuseronly(allowed_roles=[True])
def account_deleteStaff(request, pk):
    item = User.objects.get(id=pk)

    if request.method == "POST":
        item.delete()
        return redirect("dashboard-staff")

    context = {"item": item}
    return render(request, "dashboard/account_delete.html", context)


@allowed_users(allowed_roles=[True])
def account_delete(request, pk):
    item = User.objects.get(id=pk)

    if request.method == "POST":
        item.delete()
        return redirect("dashboard-customers")

    context = {"item": item}
    return render(request, "dashboard/account_delete.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=[True])
def item_edit(request, pk):
    item = Item.objects.get(id=pk)
    if request.method == "POST":
        form = ProductEditForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("dashboard-items")
    else:
        form = ProductEditForm(instance=item)
    context = {
        "form": form,
    }
    return render(request, "dashboard/item_edit.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=[True])
def item_delete(request, pk):
    item = Item.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        return redirect("dashboard-items")
    context = {"item": item}
    return render(request, "dashboard/item_delete.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=[True])
def booking(request):
    staff = User.objects.filter(is_staff=True)
    staff_count = staff.count()
    booking = Booking.objects.all()
    booking_count = booking.count()
    customer = User.objects.filter(is_staff=False)
    customer_count = customer.count()
    item = Item.objects.all()
    item_count = item.count()

    category = Category.objects.all()
    category_count = category.count()
    service = Service.objects.all()
    service_count = service.count()
    serviceItem = ServiceItem.objects.all()
    serviceItem_count = serviceItem.count()

    context = {
        "staff": staff,
        "staff_count": staff_count,
        "booking": booking,
        "customer_count": customer_count,
        "item_count": item_count,
        "booking_count": booking_count,
        "category": category,
        "category_count": category_count,
        "service": service,
        "service_count": service_count,
        "serviceItem": serviceItem,
        "serviceItem_count": serviceItem_count,
    }
    return render(request, "dashboard/booking.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=[True])
def booking_reject(request, pk):
    item = Booking.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        return redirect("dashboard-booking")
    context = {"item": item}
    return render(request, "dashboard/booking_reject.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=[True])
def booking_deleteRecord(request, pk):
    item = Booking.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        return redirect("dashboard-booking")
    context = {"item": item}
    return render(request, "dashboard/booking_deleteRecord.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=[True])
def booking_approve(request, pk):
    booking = Booking.objects.get(id=pk)
    # booking.item = Booking.objects.get(id=pk)
    if request.method == "POST":
        if booking.item:
            booking.item.status = "Occupied"
            booking.item.save()

        booking.bookingStatus = "Active"
        booking.save()
        return redirect("dashboard-booking")
    context = {"item": booking}
    return render(request, "dashboard/booking_approve.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=[True])
def booking_complete(request, pk):
    booking = Booking.objects.get(id=pk)
    # booking.item = Booking.objects.get(id=pk)
    if request.method == "POST":
        if booking.item:
            booking.item.status = "Available"
            booking.item.save()

        booking.bookingStatus = "Completed"
        booking.save()
        return redirect("dashboard-booking")
    context = {"booking": booking}
    return render(request, "dashboard/complete_booking.html", context)


# service
@login_required(login_url="user-login")
@allowed_users(allowed_roles=[True])
def service(request):
    staff = User.objects.filter(is_staff=True)
    staff_count = staff.count()
    item = Item.objects.all()
    item_count = item.count()
    customer = User.objects.filter(is_staff=False)
    customer_count = customer.count()
    booking = Booking.objects.all()
    booking_count = booking.count()
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
        "item": item,
        "form": form,
        "staff": staff,
        "category": category,
        "staff_count": staff_count,
        "customer_count": customer_count,
        "item_count": item_count,
        "booking_count": booking_count,
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
    item = Item.objects.all()
    item_count = item.count()
    customer = User.objects.filter(is_staff=False)
    customer_count = customer.count()
    booking = Booking.objects.all()
    booking_count = booking.count()
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
        "item": item,
        "form": form,
        "staff": staff,
        "category": category,
        "staff_count": staff_count,
        "customer_count": customer_count,
        "item_count": item_count,
        "booking_count": booking_count,
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

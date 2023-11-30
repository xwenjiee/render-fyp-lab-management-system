from django.utils import timezone
from django import forms
from .models import Item, Booking, Category, ServiceItem, Service
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields["desc"].required = False

    name = forms.CharField()

    def clean_name(self):
        name = self.cleaned_data.get("name", "")
        if Category.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError(
                (f"{name} already exists."), params={"name": name}
            )
        return name

    class Meta:
        model = Category
        fields = "__all__"


class CategoryEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryEditForm, self).__init__(*args, **kwargs)
        self.fields["desc"].required = False

    name = forms.CharField()

    def clean_name(self):
        cleaned_data = super().clean()
        name = self.cleaned_data.get("name", "")
        if (
            Category.objects.exclude(pk=self.instance.pk)
            .filter(name=cleaned_data.get("name"))
            .exists()
        ):
            raise forms.ValidationError(
                (f"Category with name '{name}' already exists."),
                params={"name": name},
            )
        return name

    class Meta:
        model = Category
        fields = "__all__"


class ServiceItemEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ServiceItemEditForm, self).__init__(*args, **kwargs)
        self.fields["desc"].required = False
        self.fields["serialNumber"].widget.attrs["id"] = "serialNumber"

    # serialNumber = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        serialNumber = self.cleaned_data.get("serialNumber", "")
        if (
            ServiceItem.objects.exclude(pk=self.instance.pk)
            .filter(serialNumber=cleaned_data.get("serialNumber"))
            .exists()
            and serialNumber != None
        ):
            raise forms.ValidationError(
                (f"Service Item with serial number '{serialNumber}' already exists."),
                params={"serialNumber": serialNumber},
            )
        if (
            Item.objects.filter(serialNumber=cleaned_data.get("serialNumber")).exists()
            and serialNumber != None
        ):
            raise forms.ValidationError(
                (
                    f"Service Item with {serialNumber} already exists as an Inventory Item."
                ),
                params={"serialNumber": serialNumber},
            )

        return cleaned_data

    class Meta:
        model = ServiceItem
        fields = [
            "serialNumber",
            "name",
            "desc",
        ]


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields["serialNumber"].required = False
        self.fields["category"].required = False
        self.fields["serialNumber"].widget.attrs["id"] = "serialNumber"

    # serialNumber = forms.CharField()

    def clean_serialNumber(self):
        serialNumber = self.cleaned_data.get("serialNumber", "")
        if (
            Item.objects.filter(serialNumber__iexact=serialNumber).exists()
            and serialNumber != None
        ):
            raise forms.ValidationError(
                (f"Item with serial number '{serialNumber}' already exists."),
                params={"serialNumber": serialNumber},
            )
        if (
            ServiceItem.objects.filter(serialNumber__iexact=serialNumber).exists()
            and serialNumber != None
        ):
            raise forms.ValidationError(
                (
                    f"Item with serial number '{serialNumber}' already exists as a Service Item."
                ),
                params={"serialNumber": serialNumber},
            )
        return serialNumber

    class Meta:
        model = Item
        fields = ["serialNumber", "name", "consumable", "quantity", "category"]

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get("quantity")
        serialNumber = cleaned_data.get("serialNumber")

        if serialNumber and quantity > 1:
            raise forms.ValidationError("Serial numbers are unique to 1 item only.")
        if serialNumber and quantity == 0:
            raise forms.ValidationError(
                (f"Item with serial number '{serialNumber}' already exists."),
                params={"serialNumber": serialNumber},
            )
        return cleaned_data


class ProductEditForm(forms.ModelForm):
    # serialNumber = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(ProductEditForm, self).__init__(*args, **kwargs)
        self.fields["category"].required = False
        self.fields["serialNumber"].required = False
        self.fields["serialNumber"].widget.attrs["id"] = "serialNumber"

    class Meta:
        model = Item
        fields = ["serialNumber", "name", "consumable", "quantity", "category"]

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get("quantity")
        serialNumber = cleaned_data.get("serialNumber")
        if serialNumber and quantity > 1:
            raise forms.ValidationError("Serial numbers are unique to 1 item only.")
        if serialNumber and quantity == 0:
            raise forms.ValidationError(
                "Items with serial numbers cannot have quantity of 0."
            )
        if (
            Item.objects.exclude(pk=self.instance.pk)
            .filter(serialNumber=cleaned_data.get("serialNumber"))
            .exists()
            and serialNumber != None
        ):
            raise forms.ValidationError(
                (f"Item with serial number '{serialNumber}' already exists."),
                params={"serialNumber": serialNumber},
            )
        if (
            ServiceItem.objects.filter(
                serialNumber=cleaned_data.get("serialNumber")
            ).exists()
            and serialNumber != None
        ):
            raise forms.ValidationError(
                (
                    f"Item with serial number '{serialNumber}' already exists as a Service Item."
                ),
                params={"serialNumber": serialNumber},
            )

        return cleaned_data


class ServiceItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ServiceItemForm, self).__init__(*args, **kwargs)
        self.fields["desc"].required = False
        self.fields["serialNumber"].widget.attrs["id"] = "serialNumber"

    def clean_serialNumber(self):
        serialNumber = self.cleaned_data.get("serialNumber", "")
        if ServiceItem.objects.filter(serialNumber__iexact=serialNumber).exists():
            raise forms.ValidationError(
                (f"Service Item with {serialNumber} already exists."),
                params={"serialNumber": serialNumber},
            )
        if Item.objects.filter(serialNumber__iexact=serialNumber).exists():
            raise forms.ValidationError(
                (
                    f"Service Item with {serialNumber} already exists as an Inventory Item."
                ),
                params={"serialNumber": serialNumber},
            )
        return serialNumber

    class Meta:
        model = ServiceItem
        fields = [
            "serialNumber",
            "name",
            "desc",
        ]


class ServiceItemEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ServiceItemEditForm, self).__init__(*args, **kwargs)
        self.fields["desc"].required = False
        self.fields["serialNumber"].widget.attrs["id"] = "serialNumber"

    # serialNumber = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        serialNumber = self.cleaned_data.get("serialNumber", "")
        if (
            ServiceItem.objects.exclude(pk=self.instance.pk)
            .filter(serialNumber=cleaned_data.get("serialNumber"))
            .exists()
            and serialNumber != None
        ):
            raise forms.ValidationError(
                (f"Service Item with serial number '{serialNumber}' already exists."),
                params={"serialNumber": serialNumber},
            )
        if (
            Item.objects.filter(serialNumber=cleaned_data.get("serialNumber")).exists()
            and serialNumber != None
        ):
            raise forms.ValidationError(
                (
                    f"Service Item with {serialNumber} already exists as an Inventory Item."
                ),
                params={"serialNumber": serialNumber},
            )

        return cleaned_data

    class Meta:
        model = ServiceItem
        fields = [
            "serialNumber",
            "name",
            "desc",
        ]


class ServiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.fields["desc"].required = False

    name = forms.CharField()

    def clean_name(self):
        name = self.cleaned_data.get("name", "")
        if Service.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError(
                (f"Service with {name} already exists."),
                params={"name": name},
            )
        return name

    class Meta:
        model = Service
        fields = "__all__"


class ServiceEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ServiceEditForm, self).__init__(*args, **kwargs)
        self.fields["desc"].required = False

    name = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        name = self.cleaned_data.get("name", "")
        if (
            Service.objects.exclude(pk=self.instance.pk)
            .filter(name=cleaned_data.get("name"))
            .exists()
        ):
            raise forms.ValidationError(
                (f"Service with {name} already exists."),
                params={"name": name},
            )

        return cleaned_data

    class Meta:
        model = Service
        fields = "__all__"


class ServiceBookingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ServiceBookingForm, self).__init__(*args, **kwargs)
        self.fields["service"].required = False
        self.fields["item"].required = False

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

        self.fields["item"].queryset = final

        # CONDITION:
        #   no one else requesting, or somebody has requested but it is already returned. NOT IN ANY BOOKINGS YET, but its ok if its in bookings that are "Completed"

    class Meta:
        model = Booking
        fields = [
            "item",
            "service",
            "startDateTime",
            "endDateTime",
        ]

        widgets = {
            "startDateTime": forms.TextInput(attrs={"type": "datetime-local"}),
            "endDateTime": forms.TextInput(attrs={"type": "datetime-local"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get("item")
        service = cleaned_data.get("service")
        startDateTime = cleaned_data.get("startDateTime")
        endDateTime = cleaned_data.get("endDateTime")

        if item and service:
            raise forms.ValidationError(
                "Please fill either item or service to be booked, but not both."
            )
        elif item == None and service == None:
            raise forms.ValidationError(
                "Please fill either one of item or service to be booked."
            )

        if startDateTime > endDateTime:
            raise forms.ValidationError(
                "Ending date and time cannot be earlier than starting date and time."
            )
        if startDateTime < timezone.now():
            raise forms.ValidationError("You cannot make a booking from the past!")

        return cleaned_data


class StaffForm(UserCreationForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True

    def clean_email(self):
        email = self.cleaned_data.get("email", "")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError((f"{email} is taken."), params={"email": email})
        return email

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]


# manual assign
# class ServiceBookingForm(forms.ModelForm):
#     item = forms.ChoiceField(required=False, choices=[])

#     def __init__(self, *args, **kwargs):
#         super(ServiceBookingForm, self).__init__(*args, **kwargs)
#         self.fields["service"].required = False
#         self.fields["item"].required = False
#         self.fields["item"].choices = [
#             (yr, yr)
#             for yr in ServiceItem.objects.values_list(
#                 "name",
#                 flat=True,
#             ).distinct()
#         ] + [("", "---Please select your color---")]

#         # self.fields["item"].queryset = (
#         #     ServiceItem.objects.all().values_list("name").distinct()
#         # )

#     # item = forms.ModelChoiceField(
#     #     queryset=ServiceItem.objects.all().values_list("name", "name").distinct(),
#     #     required=False,
#     # )

#     class Meta:
#         model = Booking
#         fields = [
#             "item",
#             "service",
#             "startDate",
#             "startTime",
#             "endDate",
#             "endTime",
#         ]

#         widgets = {
#             "startTime": forms.TextInput(attrs={"type": "time"}),
#             "endTime": forms.TextInput(attrs={"type": "time"}),
#             "startDate": forms.TextInput(attrs={"type": "date"}),
#             "endDate": forms.TextInput(attrs={"type": "date"}),
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         item = cleaned_data.get("item")
#         service = cleaned_data.get("service")

#         if item and service:
#             raise forms.ValidationError(
#                 "Please fill either item or service to be booked, but not both."
#             )
#         elif item == None and service == None:
#             raise forms.ValidationError(
#                 "Please fill either one of item or service to be booked."
#             )

#         return cleaned_data


# class ServiceItemBookingForm(forms.ModelForm):
#     class Meta:
#         model = Booking
#         fields = [
#             "item",
#             "service" "startDate",
#             "startTime",
#             "endDate",
#             "endTime",
#         ]
#         widgets = {
#             "startTime": forms.TextInput(attrs={"type": "time"}),
#             "endTime": forms.TextInput(attrs={"type": "time"}),
#             "startDate": forms.TextInput(attrs={"type": "date"}),
#             "endDate": forms.TextInput(attrs={"type": "date"}),
#         }

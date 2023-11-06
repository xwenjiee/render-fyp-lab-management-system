from django import forms
from .models import Item, Booking, Category, ServiceItem, Service
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CategoryForm(forms.ModelForm):
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


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields["serialNumber"].required = False
        self.fields["category"].required = False

    serialNumber = forms.CharField()

    def clean_serialNumber(self):
        serialNumber = self.cleaned_data.get("serialNumber", "")
        if (
            Item.objects.filter(serialNumber__iexact=serialNumber).exists()
            and serialNumber != ""
        ):
            raise forms.ValidationError(
                (f"Item with serial number '{serialNumber}' already exists."),
                params={"serialNumber": serialNumber},
            )
        if (
            ServiceItem.objects.filter(serialNumber__iexact=serialNumber).exists()
            and serialNumber != ""
        ):
            raise forms.ValidationError(
                (
                    f"Item with serial number '{serialNumber}' already exists as a Service Item."
                ),
                params={"serialNumber": serialNumber},
            )
        return serialNumber

    # def clean_quantity(self):
    #     quantity = self.cleaned_data.get("quantity", "")
    #     serialNumber = self.cleaned_data.get("serialNumber", "")
    #     if serialNumber != "" and quantity == 0:
    #         raise forms.ValidationError(
    #             (f"Items with serial numbers cannot have quantity of 0."),
    #             params={"serialNumber": serialNumber},
    #         )
    #     return serialNumber, quantity

    # def exempt_zero(value):
    #     if value == 0:
    #         raise ValidationError(
    #             ("Please enter a value greater than 0"),
    #             params={"value": value},
    #         )
    class Meta:
        model = Item
        fields = "__all__"

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
    serialNumber = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(ProductEditForm, self).__init__(*args, **kwargs)
        self.fields["category"].required = False
        self.fields["serialNumber"].required = False

    class Meta:
        model = Item
        fields = "__all__"

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
            and serialNumber != ""
        ):
            raise forms.ValidationError(
                (f"Item with serial number '{serialNumber}' already exists."),
                params={"serialNumber": serialNumber},
            )
        if (
            ServiceItem.objects.filter(
                serialNumber=cleaned_data.get("serialNumber")
            ).exists()
            and serialNumber != ""
        ):
            raise forms.ValidationError(
                (
                    f"Item with serial number '{serialNumber}' already exists as a Service Item."
                ),
                params={"serialNumber": serialNumber},
            )

        return cleaned_data


class ServiceItemForm(forms.ModelForm):
    serialNumber = forms.CharField()

    def clean_serialNumber(self):
        serialNumber = self.cleaned_data.get("serialNumber", "")
        if ServiceItem.objects.filter(serialNumber__iexact=serialNumber).exists():
            raise forms.ValidationError(
                (f"Service Item with {serialNumber} already exists."),
                params={"serialNumber": serialNumber},
            )
        if Item.objects.filter(serialNumber__iexact=serialNumber).exists():
            raise forms.ValidationError(
                (f"Item with {serialNumber} already exists as an Inventory Item."),
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
    serialNumber = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        serialNumber = self.cleaned_data.get("serialNumber", "")
        if (
            ServiceItem.objects.exclude(pk=self.instance.pk)
            .filter(serialNumber=cleaned_data.get("serialNumber"))
            .exists()
            and serialNumber != ""
        ):
            raise forms.ValidationError(
                (f"Item with serial number '{serialNumber}' already exists."),
                params={"serialNumber": serialNumber},
            )
        if (
            Item.objects.filter(serialNumber=cleaned_data.get("serialNumber")).exists()
            and serialNumber != ""
        ):
            raise forms.ValidationError(
                (f"Item with {serialNumber} already exists as an Inventory Item."),
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


class ServiceBookingForm(forms.ModelForm):
    # # item = forms.ChoiceField(required=False, choices=[])
    # startDateTime = forms.DateTimeField(input_formats=["%d/%m/%Y %H:%M"])

    def __init__(self, *args, **kwargs):
        super(ServiceBookingForm, self).__init__(*args, **kwargs)
        self.fields["service"].required = False
        self.fields["item"].required = False
        # super().get_form_class().base_fields["item"].limit_choices_to = {
        #     "item": ServiceItem.objects.all().values_list("name").distinct()
        # }

        #         serviceItem = ServiceItem.objects.all()
        # methods = project_main.methods_set.all() # All the Methods related to the instance
        # things = project_main.things_set.all() # All the Methods related to the instance
        # more_stuffs = project_main.morestuff_set.all() # All the Methods related to the instance
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

        # self.fields["item"].choices = [
        #     (yr, yr)
        #     for yr in ServiceItem.objects.values_list(
        #         "name",
        #         flat=True,
        #     ).distinct()
        # ] + [("", "---Please select your color---")]

        # self.fields["item"].queryset = (
        #     ServiceItem.objects.all().values_list("name").distinct()
        # )

    # item = forms.ModelChoiceField(
    #     queryset=ServiceItem.objects.all().values_list("name", "name").distinct(),
    #     required=False,
    # )

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

        return cleaned_data


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


class StaffForm(UserCreationForm):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get("email", "")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError((f"{email} is taken."), params={"email": email})
        return email

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]

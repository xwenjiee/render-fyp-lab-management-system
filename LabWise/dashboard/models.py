from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, null=True)
    desc = models.CharField("Description", max_length=500, null=True)

    def __str__(self):
        return f"{self.name}"


class Item(models.Model):
    def exempt_zero(value):
        if value == 0:
            raise ValidationError(
                ("Please enter a value greater than 0"),
                params={"value": value},
            )

    name = models.CharField(max_length=100, null=True)
    serialNumber = models.CharField(
        "Serial Number", max_length=500, null=True, default=None
    )
    consumable = models.BooleanField(null=False)
    quantity = models.PositiveIntegerField(null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, default=None
    )

    # category = models.CharField(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name}"


class ServiceItem(models.Model):
    name = models.CharField(max_length=100, null=True)
    desc = models.CharField("Description", max_length=500, null=True)
    serialNumber = models.CharField("Serial Number", max_length=500, null=False)
    status = models.CharField(default="Available", null=False)

    def __str__(self):
        return f"{self.name}"


class Service(models.Model):
    name = models.CharField(max_length=100, null=True)
    desc = models.CharField("Description", max_length=500, null=True)

    def __str__(self):
        return f"{self.name}"


class Booking(models.Model):
    # item = models.CharField(max_length=500, null=True, default=None)
    # item_assign = models.ForeignKey(
    #     ServiceItem, on_delete=models.CASCADE, null=True, default=None
    # )
    item = models.ForeignKey(
        ServiceItem, on_delete=models.CASCADE, null=True, default=None
    )
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, null=True, default=None
    )
    startDateTime = models.DateTimeField(null=True)
    endDateTime = models.DateTimeField(null=True)
    bookingStatus = models.CharField(default="Pending Approval", null=False)
    # order_quantity = models.PositiveIntegerField(null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.customer}-{self.name}"


# class Product(models.Model):
#     name = models.CharField(max_length=100, null=True)
#     quantity = models.PositiveIntegerField(null=True)
#     category = models.CharField(max_length=50, choices=CATEGORY, null=True)

#     def __str__(self):
#         return f"{self.name}"

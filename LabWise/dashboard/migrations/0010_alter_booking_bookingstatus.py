# Generated by Django 4.2.3 on 2023-10-31 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_alter_booking_item_alter_booking_service_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='bookingStatus',
            field=models.CharField(default='Pending Approval'),
        ),
    ]

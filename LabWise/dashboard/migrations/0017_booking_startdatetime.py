# Generated by Django 4.2.3 on 2023-11-02 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_remove_booking_item_assign_alter_booking_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='startDateTime',
            field=models.DateTimeField(null=True),
        ),
    ]
# Generated by Django 4.1.3 on 2023-01-26 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0006_order"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="product",
            field=models.CharField(default="", max_length=100),
        ),
    ]
# Generated by Django 3.0.6 on 2020-06-26 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_order_billing_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingaddress',
            name='city',
            field=models.CharField(default='Lagos', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='number',
            field=models.IntegerField(default=234),
            preserve_default=False,
        ),
    ]

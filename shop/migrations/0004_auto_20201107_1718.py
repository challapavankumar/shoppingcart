# Generated by Django 3.1.2 on 2020-11-07 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_adminuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_completed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('cashondelivary', 'cashondelivary'), ('khalti', 'kalthi')], default='cashondelivary', max_length=30),
        ),
    ]

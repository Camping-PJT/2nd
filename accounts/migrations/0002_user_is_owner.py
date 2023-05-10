# Generated by Django 3.2.18 on 2023-05-10 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_owner',
            field=models.CharField(choices=[('owner', '사장님'), ('customer', '고객')], default='customer', max_length=10),
        ),
    ]

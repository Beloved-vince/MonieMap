# Generated by Django 4.1.4 on 2023-07-31 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, default=1, max_length=12, unique=True),
            preserve_default=False,
        ),
    ]
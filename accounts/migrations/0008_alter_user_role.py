# Generated by Django 5.1.3 on 2024-11-20 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(2, 'customer'), (1, 'Vendor')], null=True),
        ),
    ]
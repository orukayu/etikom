# Generated by Django 5.0.3 on 2024-09-04 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etikom', '0017_alter_iade_options_alter_kargo_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='kargo',
            name='Stokkodu',
            field=models.CharField(max_length=25, null=True),
        ),
    ]

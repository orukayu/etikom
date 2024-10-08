# Generated by Django 5.0.3 on 2024-08-12 21:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etikom', '0014_kargo_tur_siparis_tur'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Iade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Siparisno', models.CharField(max_length=25)),
                ('Stokkodu', models.CharField(max_length=25)),
                ('Adet', models.PositiveIntegerField()),
                ('Desi', models.IntegerField()),
                ('Kargotutari', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Toplam', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Tur', models.CharField(max_length=20)),
                ('Firmaadi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['Siparisno'],
            },
        ),
    ]

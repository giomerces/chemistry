# Generated by Django 3.2.16 on 2022-12-30 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compounds', '0005_compound_molar_mass'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='compoundstore',
            constraint=models.UniqueConstraint(fields=('compound', 'store'), name='compound_store_unique'),
        ),
    ]
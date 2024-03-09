# Generated by Django 5.0.3 on 2024-03-09 11:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Circulation',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('checked_out_at', models.DateTimeField(help_text='Datetime at which the book was checked out by the member')),
                ('returned_at', models.DateTimeField(help_text='Datetime at which the book was returned by the member')),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='library_manager.book')),
                ('member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='library_manager.member')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('reserved_at', models.DateTimeField(help_text='Datetime at which the book was reserved by the member')),
                ('fulfilled_at', models.DateTimeField(help_text='Datetime at which the reservation was fulfilled')),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='library_manager.book')),
                ('member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='library_manager.member')),
            ],
        ),
    ]

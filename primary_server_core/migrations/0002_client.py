# Generated by Django 4.2.10 on 2024-02-22 16:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('primary_server_core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('rsa_pub_pem', models.CharField(blank=True, max_length=512, null=True, unique=True, verbose_name='RSA public pem key')),
            ],
        ),
    ]

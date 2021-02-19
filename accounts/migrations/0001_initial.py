# Generated by Django 3.1.6 on 2021-02-18 22:46

import accounts.managers
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('name', models.CharField(max_length=512, verbose_name='name')),
                ('description', models.CharField(max_length=1000, verbose_name='description')),
                ('email', models.EmailField(max_length=1000, unique=True, verbose_name='email')),
                ('btc_wallet_address', models.CharField(max_length=35, verbose_name='btc wallet address')),
                ('btc_wallet_balance', models.DecimalField(decimal_places=10, default=Decimal('0E-10'), max_digits=18, verbose_name='btc wallet balance')),
                ('eth_wallet_address', models.CharField(max_length=42, verbose_name='eth wallet address')),
                ('eth_wallet_balance', models.DecimalField(decimal_places=10, default=Decimal('0E-10'), max_digits=18, verbose_name='eth wallet balance')),
                ('max_amount_per_transaction', models.DecimalField(decimal_places=2, default=Decimal('10000'), max_digits=10, verbose_name='max amount per transaction')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', accounts.managers.UserManager()),
            ],
        ),
    ]

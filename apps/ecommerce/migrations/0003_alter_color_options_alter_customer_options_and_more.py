# Generated by Django 5.0.3 on 2024-04-05 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_remove_product_stock'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='color',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['user']},
        ),
        migrations.AlterModelOptions(
            name='employee',
            options={'ordering': ['user']},
        ),
        migrations.AlterModelOptions(
            name='gender',
            options={'ordering': ['-name']},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-created_at', 'name']},
        ),
        migrations.AlterModelOptions(
            name='productcategory',
            options={'ordering': ['-created_at', 'name', 'description']},
        ),
        migrations.AlterModelOptions(
            name='sale',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='size',
            options={'ordering': ['name']},
        ),
        migrations.RenameField(
            model_name='product',
            old_name='category',
            new_name='categories',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='color',
            new_name='colors',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='gender',
            new_name='genders',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='size',
            new_name='sizes',
        ),
    ]

# Generated by Django 5.1 on 2024-08-24 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0003_alter_cloth_gender_alter_cloth_material_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cloth',
            name='image',
            field=models.ImageField(upload_to='clothes_images/'),
        ),
        migrations.AlterField(
            model_name='cloth',
            name='material',
            field=models.CharField(choices=[('Cotton', 'Cotton'), ('Jeans', 'Jeans'), ('Denim', 'Denim'), ('Woolen', 'Woolen'), ('Nylon', 'Nylon'), ('Synthetic', 'Synthetic'), ('Mix', 'Mix')], max_length=20),
        ),
        migrations.AlterField(
            model_name='cloth',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]

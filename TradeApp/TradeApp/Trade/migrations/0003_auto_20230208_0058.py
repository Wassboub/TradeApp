# Generated by Django 3.2.16 on 2023-02-08 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Trade', '0002_auto_20230207_2318'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='coininfo',
            name='Ticks',
            field=models.IntegerField(),
        ),
    ]

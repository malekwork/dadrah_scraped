# Generated by Django 5.1.1 on 2024-09-29 19:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lawyer',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('date', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('lawyer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.lawyer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='core.question')),
            ],
        ),
    ]

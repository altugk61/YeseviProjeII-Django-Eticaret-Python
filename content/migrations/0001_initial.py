# Generated by Django 3.2.2 on 2021-05-29 10:13

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('link', models.CharField(blank=True, max_length=100)),
                ('status', models.CharField(choices=[('True', 'Evet'), ('False', 'Hayır')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='content.menu')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('duyuru', 'duyuru'), ('menu', 'menu'), ('haber', 'haber'), ('etkinlik', 'etkinlik')], max_length=10)),
                ('title', models.CharField(max_length=150)),
                ('keywords', models.CharField(blank=True, max_length=255)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('detail', ckeditor_uploader.fields.RichTextUploadingField()),
                ('slug', models.SlugField(unique=True)),
                ('status', models.CharField(choices=[('True', 'Evet'), ('False', 'Hayır')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('menu', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='content.menu')),
            ],
        ),
        migrations.CreateModel(
            name='CImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50)),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.content')),
            ],
        ),
    ]

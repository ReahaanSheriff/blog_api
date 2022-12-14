# Generated by Django 3.0.6 on 2021-12-04 16:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CreateBlog',
            fields=[
                ('blog_id', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('body', models.CharField(max_length=50)),
                ('image', models.CharField(max_length=50)),
                ('like', models.BooleanField(default=False)),
                ('user_id_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

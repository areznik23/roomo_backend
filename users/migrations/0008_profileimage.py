# Generated by Django 3.1.1 on 2020-09-12 23:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20200912_1705'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='profile_pics/default-profile.jpg', upload_to='gallery_images')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_images', to='users.profile')),
            ],
        ),
    ]
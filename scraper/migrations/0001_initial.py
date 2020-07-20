# Generated by Django 3.0.8 on 2020-07-16 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scraper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Headlines', models.CharField(max_length=3000)),
                ('Links', models.TextField(default='')),
                ('Countries', models.CharField(default='', max_length=6)),
                ('Date_Uploaded', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Twitter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tweets', models.TextField(default='')),
                ('Day_Created', models.TextField(default='')),
                ('Location', models.CharField(default='', max_length=50)),
                ('User_Handle', models.CharField(default='', max_length=90)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('scraper_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='scraper.Scraper')),
            ],
            bases=('scraper.scraper',),
        ),
    ]
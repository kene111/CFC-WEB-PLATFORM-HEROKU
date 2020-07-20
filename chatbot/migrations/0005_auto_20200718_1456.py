# Generated by Django 3.0.8 on 2020-07-18 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0004_tsu_p_volc_p'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tsu_p',
            name='earth_p_ptr',
        ),
        migrations.RemoveField(
            model_name='volc_p',
            name='earth_p_ptr',
        ),
        migrations.AddField(
            model_name='tsu_p',
            name='Yes_t',
            field=models.TextField(default=' ', max_length=300),
        ),
        migrations.AddField(
            model_name='tsu_p',
            name='id',
            field=models.AutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='volc_p',
            name='Yes_v',
            field=models.TextField(default=' ', max_length=300),
        ),
        migrations.AddField(
            model_name='volc_p',
            name='id',
            field=models.AutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='earth_p',
            name='Yes_e',
            field=models.TextField(default=' ', max_length=300),
        ),
    ]

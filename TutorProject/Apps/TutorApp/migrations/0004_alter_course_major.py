# Generated by Django 4.2.6 on 2023-10-20 03:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TutorApp', '0003_major_alter_course_major'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='major',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TutorApp.major'),
        ),
    ]
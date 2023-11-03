# Generated by Django 4.2.6 on 2023-11-01 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TutorApp', '0003_alter_major_abbreviation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='class',
            old_name='classmajor',
            new_name='class_major',
        ),
        migrations.RenameField(
            model_name='class',
            old_name='coursenum',
            new_name='course_num',
        ),
        migrations.AddField(
            model_name='class',
            name='course_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
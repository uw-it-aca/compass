# Generated by Django 4.2.9 on 2024-02-02 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compass', '0015_specialprogram'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='specialprogram',
            unique_together={('student', 'access_group')},
        ),
        migrations.RemoveField(
            model_name='specialprogram',
            name='program_code',
        ),
    ]

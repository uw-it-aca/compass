# Generated by Django 4.2.9 on 2024-01-25 00:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compass', '0014_omadcontactqueue'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialProgram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program_code', models.SmallIntegerField()),
                ('program_date', models.DateField(null=True)),
                ('modified_date', models.DateTimeField(null=True)),
                ('access_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compass.accessgroup')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='compass.appuser')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compass.student')),
            ],
            options={
                'unique_together': {('student', 'program_code', 'access_group')},
            },
        ),
    ]

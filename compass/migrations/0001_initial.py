# Generated by Django 3.2.13 on 2022-06-13 22:25

from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('access_group_id', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uwnetid', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContactType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('access_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compass.accessgroup')),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('access_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compass.accessgroup')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system_key', models.CharField(max_length=50, unique=True)),
                ('programs', models.ManyToManyField(to='compass.Program')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalContact',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('noshow', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True, default=None, null=True)),
                ('actions', models.TextField(blank=True, default=None, null=True)),
                ('source', models.CharField(default='Compass', max_length=50)),
                ('pub_date', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('author', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='compass.appuser')),
                ('contact_type', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='compass.contacttype')),
                ('student', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='compass.student')),
            ],
            options={
                'verbose_name': 'historical contact',
                'verbose_name_plural': 'historical contacts',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='ContactTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('access_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compass.accessgroup')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('noshow', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True, default=None, null=True)),
                ('actions', models.TextField(blank=True, default=None, null=True)),
                ('source', models.CharField(default='Compass', max_length=50)),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('access_group', models.ManyToManyField(to='compass.AccessGroup')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compass.appuser')),
                ('contact_topics', models.ManyToManyField(null=True, to='compass.ContactTopic')),
                ('contact_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compass.contacttype')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compass.student')),
            ],
        ),
        migrations.AddIndex(
            model_name='appuser',
            index=models.Index(fields=['uwnetid'], name='compass_app_uwnetid_eaac39_idx'),
        ),
        migrations.AddIndex(
            model_name='student',
            index=models.Index(fields=['system_key'], name='compass_stu_system__11b092_idx'),
        ),
    ]

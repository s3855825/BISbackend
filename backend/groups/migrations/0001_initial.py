# Generated by Django 3.1.3 on 2020-12-21 07:36

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0003_auto_20201221_0736'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'Group',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=255)),
                ('created_time', models.DateTimeField(default=datetime.datetime(2020, 12, 21, 7, 36, 18, 518708, tzinfo=utc))),
                ('deadline', models.DateTimeField(default=None)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customuser')),
            ],
            options={
                'db_table': 'Task',
            },
        ),
        migrations.CreateModel(
            name='TaskMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customuser')),
                ('task_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.task')),
            ],
            options={
                'db_table': 'TaskMember',
            },
        ),
        migrations.CreateModel(
            name='GroupTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.group')),
                ('task_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.task')),
            ],
            options={
                'db_table': 'GroupTask',
            },
        ),
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.group')),
                ('member_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customuser')),
            ],
            options={
                'db_table': 'GroupMember',
            },
        ),
    ]
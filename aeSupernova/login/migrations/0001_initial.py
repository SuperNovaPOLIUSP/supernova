# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('idlog', models.AutoField(serialize=False, primary_key=True, db_column=b'idLog')),
                ('action', models.TextField()),
                ('time', models.DateTimeField(db_column=b'time')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': b'user_log',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('idsession', models.AutoField(serialize=False, primary_key=True, db_column=b'idSession')),
                ('start', models.DateTimeField(db_column=b'start')),
                ('end', models.DateTimeField(null=True, db_column=b'end', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': b'login_session',
                'managed': True,
            },
            bases=(models.Model,),
        ),
    ]

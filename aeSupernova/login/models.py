from django.contrib.auth.models import User
from django.db import models

class Session(models.Model):
    idsession = models.AutoField(db_column='idSession', primary_key=True)
    user = models.ForeignKey(User)
    start = models.DateTimeField(db_column='start')
    end = models.DateTimeField(db_column='end', blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'login_session'
        
class Log(models.Model):
    idlog = models.AutoField(db_column='idLog', primary_key=True)
    user = models.ForeignKey(User)
    action = models.TextField()
    time = models.DateTimeField(db_column='time')
    class Meta:
        managed = True
        db_table = 'user_log'
from __future__ import unicode_literals

from django.db import models


class UserHome(models.Model):
    uid = models.BigIntegerField(primary_key=True)
    user_name = models.CharField(max_length=255)
    home = models.CharField(max_length=255)
    lang = models.IntegerField()

    def __str__(self):
        return self.user_name

    def json(self):
        return {
            "uid": self.uid,
            "user_name": self.user_name,
            "home": self.home.encode("utf-8"),
            "lang": self.lang,
        }

from django.db import models
from django.urls import reverse # generates urls
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class AvailableTime(models.Model):
    """
    A model that represents available times for a user or group
    """
    # properties (fields)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()

    # relationships defined in the user and group models
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True)

    # meta
    class Meta:
        # order by startTime then endTime in normal order
        ordering = ["startTime", "endTime"]

    def __str__(self):
        return self.startTime.strftime('%I:%M %p |  %m/%d/%y ') + " to " + self.endTime.strftime('%I:%M %p |  %m/%d/%y ')



class User(AbstractUser):
    """
    A model that represents users
    """
    # properties (fields)

    # relationships (the group relationship is defined in the group model)

    # meta
    # class Meta:
    #     # order by name
    #     ordering = ["user.first_name", "user.last_name"]

    # methods
    # def __str__(self):
    #     return " {0} {1}".format(self.first_name, self.last_name)


class ScheduleHubGroup(models.Model):
    """
    A model that represents a group of users
    """
    # properties (fields)
    name = models.CharField(max_length=128, help_text="Enter a name")

    # relationships
    times = models.ForeignKey(AvailableTime,on_delete=models.SET_NULL, null=True)
    users = models.ManyToManyField(User)

    # meta
    class Meta:
        # order by name
        ordering = ["name"]

    # Methods
    # def get_absolute_url(self):
    #     return reverse('scheduleHub')

    def __str__(self):
        return self.name


"""
So I need models
    - user 
        - name
        - many to many: groups that the user belongs to
        - one to many: available times
    - group
        - name
        - one to many: time available for all # a data cache
        - many to many: users that are part of the group
    - time
        - one to one: user
        - one to one: group
        - start time
        - end time
"""
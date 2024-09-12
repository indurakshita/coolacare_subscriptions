from django.db import models

class AvailableSlots(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.CharField(max_length=255)
    daytime = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    total_slots = models.IntegerField()
    available_slots = models.IntegerField()
    booked_slots = models.IntegerField(default=0)
   

    def __str__(self):
        return f"{self.day} - {self.daytime} - {self.time}"
    
    
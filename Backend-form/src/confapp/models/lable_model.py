from django.db import models

class UILabel(models.Model):
    id = models.AutoField(primary_key=True)
    page_name = models.CharField(max_length=255)
    key = models.CharField(max_length=255,default="")
    type = models.CharField(max_length=255)
    display_value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.page_name} - {self.type}"
    



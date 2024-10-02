from django.db import models

class DateRange(models.Model):
    from_date = models.DateField()
    to_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.from_date} to {self.to_date}"

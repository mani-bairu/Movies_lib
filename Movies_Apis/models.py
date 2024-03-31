from django.db import models

# Create your models here.

status_choices=(
    ('coming-up','coming-up'),
    ('starting','starting'),
    ('running','running'),
    ('finished','finished'),

)

class Movie(models.Model):
    name=models.CharField(max_length=100)
    protagonists=models.TextField()
    release_date=models.DateField()
    status=models.CharField(max_length=100,choices=status_choices, default='coming-up')
    poster=models.ImageField(upload_to='posters',null=True)
    trailer=models.FileField(upload_to='trailers',null=True)
    rating=models.BigIntegerField(null=True,default=0)

    def __str__(self):
        return self.name

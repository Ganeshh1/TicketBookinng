from django.db import models
import datetime

class Theater(models.Model):
    name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Movies(models.Model):
    name=models.CharField(max_length=100)    
    movie_image=models.ImageField(default='default.jpg',upload_to='movies')
    theater_name=models.ForeignKey(Theater,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name+' in '+str(self.theater_name))

    class Meta:
        verbose_name_plural = "Movies"
        ordering = ['name']

class ShowTiming(models.Model):
    showtime=models.DateTimeField(default=datetime.datetime.now())
    movie=models.ForeignKey(Movies,on_delete=models.CASCADE)
    count=models.IntegerField(default=150)

    def __str__(self):
        return str(str(self.showtime)+ ' '+ str(self.movie)+' '+str(self.count))






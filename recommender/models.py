from django.db import models

class Paper(models.Model):
    title = models.CharField(max_length=500) #name of paper

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

class Researcher(models.Model):
    name = models.CharField(max_length=100) #name of researcher
    papers = models.ManyToManyField(Paper) #connecting back to their papers

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

# Create your models here.

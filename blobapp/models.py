from django.db import models
from django import forms


class MapFile(models.Model):
    name = models.CharField(max_length=255, blank=True)
    map_file = models.FileField(upload_to='maps/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Job(models.Model):
    submit_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(blank=True, null=True)
    completion_time = models.DateTimeField(blank=True, null=True)
    query_map_file = models.ForeignKey(MapFile, on_delete=models.CASCADE)
    query_points_file = models.CharField(max_length=100)
    stage = models.IntegerField(default=0)
    result_json_file = models.CharField(max_length=100)

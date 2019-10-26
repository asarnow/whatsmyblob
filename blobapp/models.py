from django.db import models


class Job(models.Model):
    submit_time = models.DateTimeField()
    start_time = models.DateTimeField()
    completion_time = models.DateTimeField()
    query_map_file = models.CharField(max_length=100)
    query_points_file = models.CharField(max_length=100)


class Result(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    json_file = models.CharField(max_length=100)

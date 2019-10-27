from django.db import models


class Job(models.Model):
    submit_time = models.DateTimeField()
    start_time = models.DateTimeField()
    completion_time = models.DateTimeField()
    query_map_file = models.CharField(max_length=300)
    query_points_file = models.CharField(max_length=100)
    stage = models.IntegerField()
    result_json_file = models.CharField(max_length=100)



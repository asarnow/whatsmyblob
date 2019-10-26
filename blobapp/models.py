from django.db import models


class Job(models.Model):
    uid = ""
    submit_time = 0
    start_time = 0
    completion_time = 0
    query_map_file = ""
    query_points_file = ""


class Result(models.Model):
    uid = ""
    job_uid = ""
    json_file = ""

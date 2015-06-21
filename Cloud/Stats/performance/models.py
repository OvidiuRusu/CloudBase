from django.db import models


class PcInfo(models.Model):
    pc_name = models.CharField(max_length=50)
    ip = models.CharField(max_length=50)


class Performance(models.Model):
    pc = models.ForeignKey(PcInfo, default=1)
    cpu_percent = models.IntegerField(default=0)
    memory_percent = models.IntegerField(default=0)
    disk_percent = models.IntegerField(default=0)


class Statistic(models.Model):
    pc = models.ForeignKey(PcInfo, default=1)
    process_name = models.CharField(max_length=50)
    cpu = models.FloatField(default=0)
    memory = models.FloatField(default=0)
    reads = models.BigIntegerField(default=0)
    writes = models.BigIntegerField(default=0)
    threads = models.IntegerField(default=0)

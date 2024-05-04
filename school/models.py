import logging

from django.db import models
from django.db.models.signals import post_save


LOGGER = logging.getLogger(__name__)


class Student(models.Model):
    name = models.TextField()

    @classmethod
    def post_save(cls, instance: "Student", **kwargs):
        LOGGER.info("学生数据保存了: %s", instance)


class Exam(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.IntegerField()


post_save.connect(Student.post_save, Student)

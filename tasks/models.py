from django.db import models
from authorization.models import User
STATUS_CHOICES = (
    (1, "Pending"),
    (2, "In Progress"),
    (3, "Completed"),
)


class Tasks(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    due_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('created_at',)
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)

    text = models.CharField(max_length=400)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Comment',
        verbose_name_plural = "Comments"

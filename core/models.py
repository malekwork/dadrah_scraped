from django.db import models

class Lawyer(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.title

class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    lawyer = models.ForeignKey(Lawyer, on_delete=models.SET_NULL, null=True)
    text = models.TextField()

    def __str__(self):
        return f"Answer by {self.lawyer.name} to {self.question.title}"

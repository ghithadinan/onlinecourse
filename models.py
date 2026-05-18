from django.db import models


class Question(models.Model):
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,   # wajib untuk ForeignKey
        related_name='questions'
    )
    question_text = models.CharField(max_length=500)
    grade = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,   # wajib untuk ForeignKey
        related_name='choices'
    )
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey(
        'Enrollment',
        on_delete=models.CASCADE    # wajib untuk ForeignKey
    )
    choices = models.ManyToManyField(Choice)
    submission_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission #{self.id}"
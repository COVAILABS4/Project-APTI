from django.db import models


class User(models.Model):
    user_id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    dob = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    photo_url = models.ImageField(upload_to="images/", default="images/krishtec.jpg")
    type = models.CharField(
        max_length=255, default="tech"
    )  # New field for tech/non-tech/user

    def save(self, *args, **kwargs):
        if not self.photo_url:
            self.photo_url.name = f"images/{self.user_id}.jpg"
        super().save(*args, **kwargs)


class Topic(models.Model):
    topic_id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.CharField(max_length=255)
    domain_type = models.CharField(
        max_length=10,
        default="tech",
    )
    tech_type = models.CharField(
        max_length=10,
        default="sw",
    )


class UserTopic(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_by = models.CharField(max_length=255)
    created_at = models.CharField(max_length=255)

    class Meta:
        unique_together = ("user_id", "topic_id")


class SubTopic(models.Model):
    subtopic_id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.CharField(max_length=255)


class LearningMaterial(models.Model):
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)
    subtopic_id = models.ForeignKey(SubTopic, on_delete=models.CASCADE)
    content = models.TextField()

    class Meta:
        unique_together = ("topic_id", "subtopic_id")


class Practice(models.Model):
    title_id = models.CharField(max_length=255, primary_key=True)
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)
    subtopic_id = models.ForeignKey(SubTopic, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    duration = models.IntegerField(default=900)  # Duration in seconds
    attempts = models.IntegerField(default=1)  # Number of attempts


class Test(models.Model):
    title_id = models.CharField(max_length=255, primary_key=True)
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)
    subtopic_id = models.ForeignKey(SubTopic, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    duration = models.IntegerField(default=900)  # Duration in seconds
    attempts = models.IntegerField(default=1)  # Number of attempts


class PracticeQuestion(models.Model):
    question_id = models.CharField(max_length=255, primary_key=True)
    title_id = models.ForeignKey(Practice, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    question_img = models.CharField(max_length=255, null=True, blank=True, default=None)
    correct_option = models.IntegerField()
    explanation = models.TextField()
    explanation_img = models.CharField(
        max_length=255, null=True, blank=True, default=None
    )


class TestQuestion(models.Model):
    question_id = models.CharField(max_length=255, primary_key=True)
    title_id = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    question_img = models.CharField(max_length=255, null=True, blank=True, default=None)
    correct_option = models.IntegerField()
    explanation = models.TextField()
    explanation_img = models.CharField(
        max_length=255, null=True, blank=True, default=None
    )


class PracticeOption(models.Model):
    option_id = models.CharField(max_length=255, primary_key=True)
    question_id = models.ForeignKey(PracticeQuestion, on_delete=models.CASCADE)
    option1 = models.CharField(max_length=255)
    option1_img = models.CharField(max_length=255, null=True, blank=True, default=None)
    option2 = models.CharField(max_length=255)
    option2_img = models.CharField(max_length=255, null=True, blank=True, default=None)
    option3 = models.CharField(max_length=255)
    option3_img = models.CharField(max_length=255, null=True, blank=True, default=None)
    option4 = models.CharField(max_length=255)
    option4_img = models.CharField(max_length=255, null=True, blank=True, default=None)


class TestOption(models.Model):
    option_id = models.CharField(max_length=255, primary_key=True)
    question_id = models.ForeignKey(TestQuestion, on_delete=models.CASCADE)
    option1 = models.CharField(max_length=255)
    option1_img = models.CharField(max_length=255, null=True, blank=True, default=None)
    option2 = models.CharField(max_length=255)
    option2_img = models.CharField(max_length=255, null=True, blank=True, default=None)
    option3 = models.CharField(max_length=255)
    option3_img = models.CharField(max_length=255, null=True, blank=True, default=None)
    option4 = models.CharField(max_length=255)
    option4_img = models.CharField(max_length=255, null=True, blank=True, default=None)


class TestHistory(models.Model):
    test_id = models.CharField(max_length=255, primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)
    subtopic_id = models.ForeignKey(SubTopic, on_delete=models.CASCADE)
    title_id = models.ForeignKey(Test, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    start_at = models.CharField(max_length=255)
    finished_at = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    score = models.IntegerField()
    total_question = models.IntegerField()


class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    test_id = models.ForeignKey(TestHistory, on_delete=models.CASCADE)
    report = models.JSONField()

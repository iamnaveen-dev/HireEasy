from django.db import models
from apps.users.models import User


class Question(models.Model):

    DIFFICULTY_CHOICES = (
        ('beginner', 'Beginner'),
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
        ('expert', 'Expert'),
    )

    TOPIC_CHOICES = (
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('java', 'Java'),
        ('cpp', 'C++'),
        ('golang', 'Go'),
        ('rust', 'Rust'),
        ('typescript', 'TypeScript'),
        ('django', 'Django'),
        ('fastapi', 'FastAPI'),
        ('flask', 'Flask'),
        ('nodejs', 'Node.js'),
        ('react', 'React'),
        ('nextjs', 'Next.js'),
        ('vue', 'Vue.js'),
        ('angular', 'Angular'),
        ('sql', 'SQL'),
        ('mysql', 'MySQL'),
        ('postgresql', 'PostgreSQL'),
        ('mongodb', 'MongoDB'),
        ('redis', 'Redis'),
        ('elasticsearch', 'Elasticsearch'),
        ('dsa', 'Data Structures & Algorithms'),
        ('os', 'Operating Systems'),
        ('networking', 'Computer Networks'),
        ('dbms', 'Database Management'),
        ('system_design', 'System Design'),
        ('hld', 'High Level Design'),
        ('lld', 'Low Level Design'),
        ('microservices', 'Microservices'),
        ('api_design', 'API Design'),
        ('devops', 'DevOps'),
        ('docker', 'Docker'),
        ('kubernetes', 'Kubernetes'),
        ('aws', 'AWS'),
        ('gcp', 'Google Cloud'),
        ('azure', 'Azure'),
        ('ci_cd', 'CI/CD'),
        ('machine_learning', 'Machine Learning'),
        ('deep_learning', 'Deep Learning'),
        ('nlp', 'Natural Language Processing'),
        ('computer_vision', 'Computer Vision'),
        ('mlops', 'MLOps'),
        ('llm', 'Large Language Models'),
        ('android', 'Android'),
        ('ios', 'iOS'),
        ('react_native', 'React Native'),
        ('flutter', 'Flutter'),
        ('cybersecurity', 'Cybersecurity'),
        ('web_security', 'Web Security'),
        ('cryptography', 'Cryptography'),
        ('behavioural', 'Behavioural'),
        ('leadership', 'Leadership'),
        ('problem_solving', 'Problem Solving'),
    )

    QUESTION_TYPE_CHOICES = (
        ('theoretical', 'Theoretical'),
        ('coding', 'Coding'),
        ('system_design', 'System Design'),
        ('behavioural', 'Behavioural'),
        ('debugging', 'Debugging'),
        ('case_study', 'Case Study'),
    )

    title = models.CharField(max_length=500)
    description = models.TextField()
    topic = models.CharField(
        max_length=50,
        choices=TOPIC_CHOICES
    )
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='medium'
    )
    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPE_CHOICES,
        default='theoretical'
    )
    expected_answer = models.TextField()
    follow_up_questions = models.JSONField(
        default=list,
        blank=True
    )
    tags = models.JSONField(
        default=list,
        blank=True
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    is_active = models.BooleanField(default=True)
    times_asked = models.PositiveIntegerField(default=0)
    average_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'questions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.topic} - {self.difficulty})"
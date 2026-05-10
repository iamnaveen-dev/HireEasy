from django.db import models
from apps.users.models import User


class Company(models.Model):
    INDUSTRY_CHOICES=(
        ('technology', 'Technology'),
        ('finance', 'Finance'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('ecommerce', 'E-Commerce'),
        ('gaming', 'Gaming'),
        ('consulting', 'Consulting'),
        ('startup', 'Startup'),
        ('other', 'Other'),

    )

    SIZE_CHOICES=(
         ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-500', '201-500 employees'),
        ('501-1000', '501-1000 employees'),
        ('1000+', '1000+ employees'),

    )

    name=models.CharField(max_length=255)
from django.db import models
from apps.users.models import User


class Company(models.Model):
    INDUSTRY_CHOICES = (
        ('technology', 'Technology'),
        ('finance', 'Finance'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('ecommerce', 'E-Commerce'),
        ('gaming', 'Gaming'),
        ('consulting', 'Consulting'),
        ('startup', 'Startup'),
        ('other', 'Other'),
    )

    SIZE_CHOICES = (
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-500', '201-500 employees'),
        ('501-1000', '501-1000 employees'),
        ('1000+', '1000+ employees'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField(
        blank=True,
        null=True
    )
    industry = models.CharField(
        max_length=50,
        choices=INDUSTRY_CHOICES
    )
    size = models.CharField(
        max_length=20,
        choices=SIZE_CHOICES
    )
    website = models.URLField(
        blank=True,
        null=True
    )
    logo = models.ImageField(
        upload_to='company_logos/',
        blank=True,
        null=True
    )
    admin = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='company'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'companies'
        ordering = ['-created_at']
        verbose_name_plural = 'Companies'

    def __str__(self):
        return f"{self.name} ({self.industry})"


class CompanyMember(models.Model):
    MEMBER_ROLE_CHOICES = (
        ('interviewer', 'Interviewer'),
        ('hiring_manager', 'Hiring Manager'),
        ('recruiter', 'Recruiter'),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='members'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='company_memberships'
    )
    role = models.CharField(
        max_length=20,
        choices=MEMBER_ROLE_CHOICES,
        default='interviewer'
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'company_members'
        unique_together = ('company', 'user')

    def __str__(self):
        return f"{self.user.username} at {self.company.name}"
    







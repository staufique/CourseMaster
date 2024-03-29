from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.contrib.auth.models import Permission
from .manager import CustomBaseUserManager

class Course(models.Model):
    COURSE_CHOICES = [
        ('Python', 'Python Programming'),
        ('Java', 'Java Programming'),
        ('Web', 'Web Development'),
        ('DataScience', 'Data Science'),
        ('AI', 'Artificial Intelligence'),
    ]

    name = models.CharField(max_length=100, choices=COURSE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class User(AbstractUser):
    username=None
    name=models.CharField(max_length=250,null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=14)
    dob = models.DateField(null=True)
    city = models.CharField(max_length=100)
    courses = models.ManyToManyField('Course', related_name='users')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomBaseUserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     if self.is_superuser and self.is_staff:
    #         # Remove from staff group if exists
    #         staff_group = Group.objects.get_or_create(name='Staff')[0]
    #         self.groups.remove(staff_group)
    #         # Add to superuser group with all permissions
    #         superuser_group = Group.objects.get_or_create(name='Superuser')[0]
    #         self.groups.add(superuser_group)
    #         self.user_permissions.set(Permission.objects.all())
    #     elif self.is_staff:
    #         # Remove from superuser group if exists
    #         superuser_group = Group.objects.get_or_create(name='Superuser')[0]
    #         self.groups.remove(superuser_group)
    #         # Add to staff group with specific permissions
    #         staff_group, _ = Group.objects.get_or_create(name='Staff')
    #         permissions = Permission.objects.filter(codename__in=['add_staff', 'view_staff'])
    #         staff_group.permissions.set(permissions)
    #         self.groups.add(staff_group)

    # class Meta:
    #     permissions = (
    #         ('view_staff', 'Can view staff'),
    #         ('add_staff', 'Can add staff'),
    #     )
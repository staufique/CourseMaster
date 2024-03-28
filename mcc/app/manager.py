from django.contrib.auth.models import BaseUserManager

class CustomBaseUserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
         if not email:
              raise ValueError(("email must be there"))
         
         email = self.normalize_email(email)
         user = self.model(email=email,**extra_fields)
         user.set_password(password)
         user.save(using=self._db)
         return user

    def create_superuser(self,email,password, **extra_fields):
         extra_fields.setdefault('is_staff',True)
         extra_fields.setdefault('is_active',True)
         extra_fields.setdefault('is_superuser',True)

         if extra_fields.get('is_staff') is not True:
              raise ValueError(("super user must have is_staff True"))
         
         return self.create_user(email,password,**extra_fields)
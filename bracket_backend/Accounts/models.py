from django.db import models


from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
SEX_CHOICES = (
    ('F', 'Female',),
    ('M', 'Male',),
    ('','Prefer Not To Say')
)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        user.set_password(password)

        user.save()

        return user

    

        return self.create_user(email=email, password=password, **extra_fields)

def get_opposed_sex(sex):
    return 'M' if sex == 'F' else 'F'



class User(AbstractUser):
    
    email = models.CharField(max_length=80, unique=True)
    username = models.CharField(max_length=45)
    bio=models.CharField(max_length=200,null=True,blank=True)
    age = models.IntegerField(validators=[MinValueValidator(18),MaxValueValidator(130)],db_index=True, null=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, db_index=True ,null=True)
    
    
    def __str__(self):
        return self.username

    @property
    def get_opposed_sex(self):
        return get_opposed_sex(self.sex)

    objects = CustomUserManager()
    USERNAME_FIELD = "email"


    REQUIRED_FIELDS = ["username",'age','sex',]

    def __str__(self):
        return self.username
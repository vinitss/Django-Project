from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    TYPE_CHOICES = (('Student', 'Student' ),
                    ('Faculty', 'Faculty' ),
                    ('Community', 'Community' ),
                    )
    type = models.CharField(
        max_length=9,
        choices=TYPE_CHOICES,
        default= 'Student'
    )
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    def __str__(self):
        return f'{self.user.username} Profile'
    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Student_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50,null=True,blank=False)
    last_name = models.CharField(max_length=50,null=True,blank=False)
    now = datetime.datetime.now()
    start_year=now.year-4
    end_year=now.year+1 # end_year in range is exclusive
    # hence in for loop
    # [start_year,end_year)
    # we have printed 5 years because current month is not taken into consideration
    BRANCH_CHOICES =(('Computer','Computer Engineering'),
                    ('Electrical','Electrical Engineering'),
                    ('Civil','Civil Engineering'),
                    ('I.T','I.T Engineering'),
                    ('Mechanical','Mechanical Engineering'),
                        )

    year_of_admission = models.CharField(max_length=5,choices=[(str(x),str(x)) for x in range(start_year,end_year)],default=str(start_year))
    branch = models.CharField(
        max_length=25,
        choices=BRANCH_CHOICES
    )
    roll_number = models.IntegerField(null=True,blank = True, default = None)


    def __str__(self):
        return f'{self.user.username} Student'


class Faculty_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50,null=True,blank=False)
    last_name = models.CharField(max_length=50,null=True,blank=False)

    def __str__(self):
        return f'{self.user.username} Faculty'


class Community_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=50,null=True,blank=False)

    admin_username = models.CharField(max_length=50,null=True,blank=False)

    def __str__(self):
        return f'{self.user.username} Community'









'''
from django.db import models
from django.contrib.auth.models import User,AbstractBaseUser

class UserProfile(AbstractBaseUser):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=16,null=True)
    company = models.CharField(max_length=50,null=True)
    username = models.CharField(max_length=100, unique=True , null=True)
    USERNAME_FIELD = User.username

'''

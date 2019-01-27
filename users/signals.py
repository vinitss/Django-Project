from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile,Student_Profile,Faculty_Profile,Community_Profile
import users.globalbaz

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    print ('Gm')
    print (users.globalbaz.Type)
    if created and users.globalbaz.Type =='Student':
        Student_Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_student_profile(sender, instance, created, **kwargs):
    if created and users.globalbaz.Type == 'Student':
        instance.student_profile.save()

@receiver(post_save, sender=User)
def create_faculty_profile(sender, instance, created, **kwargs):
    print ('Gm')
    print (users.globalbaz.Type)
    if created and users.globalbaz.Type =='Faculty':
        Faculty_Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_faculty_profile(sender, instance, created, **kwargs):
    if created and users.globalbaz.Type == 'Faculty':
        instance.faculty_profile.save()

@receiver(post_save, sender=User)
def create_community_profile(sender, instance, created, **kwargs):
    print ('Gm')
    print (users.globalbaz.Type)
    if created and users.globalbaz.Type =='Community':
        Community_Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_community_profile(sender, instance, created, **kwargs):
    if created and users.globalbaz.Type == 'Community':
        instance.community_profile.save()

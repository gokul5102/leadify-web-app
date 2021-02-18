from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save,post_save
# from django.contrib.auth import get_user_model 

# User=get_user_model() #A function for custom user model
class User(AbstractUser):
    is_organiser=models.BooleanField(default=True)
    is_agent=models.BooleanField(default=False)

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username



class Lead(models.Model):
    # SOURCE_CHOICES=(
    #     ('Youtube','Youtube'), #first value is stored in db,2nd is displayed on screen
    #     ('Google','Google'),
    #     ('Newsletter','Newsletter'),
    # )
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    age=models.IntegerField(default=0)
    organisation=models.ForeignKey(Profile,on_delete=models.CASCADE)#to keep track of leads within an organisation
    agent=models.ForeignKey("Agent",null=True,blank=True,on_delete=models.SET_NULL)
    category=models.ForeignKey("Category",related_name="leads",null=True,blank=True,on_delete=models.SET_NULL)
    description=models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)
    #live tracker of date and time
    
    phone_number=models.CharField(max_length=20)
    email=models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

    # phoned=models.BooleanField(default=False)
    # source=models.CharField(choices=SOURCE_CHOICES,max_length=100)

    # profile_picture=models.ImageField(blank=True,null=True) blank means ' ',null means nothing
    # special_files=models.FileField(blank=True,null=True) files are not uploaded into db


class Category(models.Model):
    name=models.CharField(max_length=30) #New,Contacted,Converted,Unconverted
    organisation=models.ForeignKey(Profile,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name}"

class Agent(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    organisation=models.ForeignKey(Profile,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email

def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
       Profile.objects.create(user=instance)

post_save.connect(post_user_created_signal,sender=User)
from django.contrib import admin
from .models import User,Lead,Agent,Profile,Category

admin.site.register(User)
admin.site.register(Lead)
admin.site.register(Agent)
admin.site.register(Profile)
admin.site.register(Category)
# Register your models here.

from django.contrib import admin
from .models import *

admin.site.register([
    User,
    Pet,
    Provider,
    Trainer,
    Service_Order,
    Payment,
    User_Avatar,
    Trainer_Avatar,
])
from datetime import datetime, UTC

from django.db import models


class User(models.Model):
    uid = models.AutoField(primary_key=True)
    l_name = models.CharField(max_length=50)
    f_name = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    dob = models.DateField()
    password = models.CharField(max_length=255)
    admin = models.BooleanField(default=False)
    description = models.CharField(max_length=15, null=True, blank=True)
    lockout = models.DateTimeField(default=datetime.fromtimestamp(0.0, UTC))
    class Meta:
        db_table = 'user'


class User_Avatar(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    avatar = models.CharField(max_length=260, null=True, blank=True)
    class Meta:
        db_table = 'user_avatar'

class Pet(models.Model):
    pid = models.AutoField(primary_key=True)
    p_name = models.CharField(max_length=25)
    species = models.CharField(max_length=25)
    breed = models.CharField(max_length=25)
    age = models.IntegerField(null=True, blank=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    diagnosis = models.CharField(max_length=500, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    class Meta:
        db_table = 'pet'

class Pet_Avatar(models.Model):
    pid = models.ForeignKey(Pet, on_delete=models.CASCADE, primary_key=True)
    avatar = models.CharField(max_length=260, null=True, blank=True)
    class Meta:
        db_table = 'pet_avatar'

class Provider(models.Model):
    provid = models.AutoField(primary_key=True)
    provider_name = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    lockout = models.DateTimeField(default=datetime.fromtimestamp(0.0, UTC))
    class Meta:
        db_table = 'provider'


class Trainer(models.Model):
    tid = models.AutoField(primary_key=True)
    provid = models.ForeignKey(Provider, on_delete=models.CASCADE)
    l_name = models.CharField(max_length=50)
    f_name = models.CharField(max_length=50)
    dob = models.DateField()
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    lockout = models.DateTimeField(default=datetime.fromtimestamp(0.0, UTC))
    class Meta:
        db_table = 'trainer'

class Trainer_Avatar(models.Model):
    tid = models.ForeignKey(Trainer, on_delete=models.CASCADE, primary_key=True)
    avatar = models.CharField(max_length=260, null=True, blank=True)
    class Meta:
        db_table = 'trainer_avatar'

class Service_Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    pid = models.ForeignKey(Pet, on_delete=models.CASCADE)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    tid = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    service_type = models.CharField(max_length=15)
    cost = models.IntegerField()
    status = models.CharField(max_length=15)
    class Meta:
        db_table = 'service_order'

class Payment(models.Model):
    paymentid = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Service_Order, on_delete=models.CASCADE)
    payment_info = models.CharField(max_length=25)
    class Meta:
        db_table = 'payment'
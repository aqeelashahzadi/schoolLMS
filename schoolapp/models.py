from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class coursesdb(models.Model):
    # courses_id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)
    detail=models.CharField(max_length=50)
    image=models.ImageField(upload_to="schoolapp/images",default="")
    def __str__(self):
        return self.name
class subjectdb(models.Model):
    id=models.AutoField(primary_key=True)
    classname=models.ForeignKey(coursesdb,on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    detail=models.CharField(max_length=50)
    image=models.ImageField(upload_to="schoolapp/images",default="")
    def __str__(self):
        return self.name
class contact_db(models.Model):
    # contacts_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)
    email=models.EmailField(max_length=50)
    phoneno=models.CharField(max_length=20)
    question=models.CharField(max_length=200)
    def __str__(self):
        return self.email

class payment_db(models.Model):
    # payments_id=models.AutoField(primary_key=True)
    email_pay=models.CharField(max_length=30,default="")
    cardnos_pay=models.IntegerField(default=0)
    cardname_pay=models.CharField(max_length=100,default="")
    seccode_pay=models.CharField(max_length=30, default="")
    exdate_pay=models.DateField()
    PAYMENT_CHOICES=(('wiretransfer','wire tranfer'),('paypal','Paypal'),('payoner','Payoner'),('creditcard','Credit card'))
    selected_option = models.CharField(max_length=20, choices=PAYMENT_CHOICES, blank=True)
    def __str__(self):
        return self.email_pay
class carts_db(models.Model):
    imges=models.ImageField(upload_to="schoolapp/images",default="")
    name=models.CharField(max_length=30)
    detail=models.CharField(max_length=50)
    userss=models.CharField(max_length=50)
    proname = models.ForeignKey(coursesdb, on_delete=models.SET_NULL, null=True, blank=True)
 
class comment_db(models.Model):
    sno=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comment=models.TextField()
    timestamp=models.DateTimeField(default=now)
    # pointing is parent comment
    parent=models.ForeignKey('self', on_delete=models.CASCADE,null=True)
    subjectname=models.ForeignKey(coursesdb,on_delete=models.CASCADE)
    


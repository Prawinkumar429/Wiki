from django.db import models
from django.core.files.base import ContentFile
from django_userforeignkey.models.fields import UserForeignKey
from django.contrib.auth.models import User



class CustomUser(User):
    class Meta:
        proxy = True  # This is important to indicate that this model is a proxy model of the User model

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    
class Wiki(models.Model):
    subject = models.CharField(max_length=200)
    description = models.TextField()
    Approval_Status = models.CharField(max_length=250,null=True,blank=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    Created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT,null=True,blank=True)
    Comments = models.CharField(max_length=1000,null=True,blank=True)
    

    def __str__(self):
        return self.subject
    
class FileUpload(models.Model):
    wiki_entry = models.ForeignKey(Wiki, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/',null=True,blank=True)

    def __str__(self):
        try:
            return self.file.name
        except FileNotFoundError:
            return "File not found"




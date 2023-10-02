from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor_uploader.fields import RichTextUploadingField 
from django.core.exceptions import ValidationError

# Create your models here.


class Skill(models.Model):
    name = models.CharField(max_length=255)
    percentage = models.IntegerField(validators=[MinValueValidator(0),
                                       MaxValueValidator(100)], default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name', 'percentage']

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 2.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max image size is %sMB" % str(megabyte_limit))
    
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blog/', default='blog/default.jpg', validators=[validate_image])
    description = RichTextUploadingField() # CKEditor Rich Text Field
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class Contact(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField()
    subject = models.CharField(max_length=100, null=True, blank=True, default=None)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_date']
    def __str__(self):
        return "{} - {}".format(self.name, self.subject)


class Newsletter(models.Model):
    email = models.EmailField()
    def __str__(self):
        return self.email
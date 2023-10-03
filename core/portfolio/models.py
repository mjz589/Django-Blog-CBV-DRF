from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField 
from django.core.exceptions import ValidationError
from datetime import date

# Create your models here.


class PortfolioCategory(models.Model):
    name = models.CharField(max_length=60, default="Web Design")
    class Meta:
        verbose_name_plural = 'Portfolio Categories'
    def __str__(self):
        return self.name


class Portfolio(models.Model):
    
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 2.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max image size is %sMB" % str(megabyte_limit))
    
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='portfolio/', default='portfolio/default.jpg', validators=[validate_image])
    description = RichTextUploadingField() # CKEditor Rich Text Field
    category = models.ForeignKey(PortfolioCategory, on_delete=models.CASCADE,)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_date',)

    def __str__(self):
        return "{} - {}".format(self.title, self.id)
    
    def get_absolute_url(self):
        return reverse('portfolio:single', kwargs={'pid':self.id})


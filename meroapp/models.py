from django.db import models  

class ApprovedPost(models.Model):  
    title = models.CharField(max_length=100)  
    image = models.ImageField(upload_to='images/')  # 'images/' is the folder where images will be stored  
    date = models.DateTimeField(auto_now_add=True)  
    description =models.TextField()
    postby= models.CharField(max_length=500,default='')
    def __str__(self):  
        return self.title 
    
class PendingPost(models.Model):
    title = models.CharField(max_length=100)  
    image = models.ImageField(upload_to='pendingimages/')  # 'images/' is the folder where images will be stored  
    date = models.DateTimeField(auto_now_add=True)  
    description = models.TextField()
    postby= models.CharField(max_length=500,default='')
    
    def __str__(self):
        return self.title
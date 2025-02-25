from django.db import models

class RecievedEmails(models.Model):
    email = models.EmailField()
    sender = models.EmailField()
    subject = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    

class Emails(models.Model):
    email = models.EmailField(unique=True)
    type = models.TextField(max_length=120, default='Potential Cust')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


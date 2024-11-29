from django.db import models

# Create your models here.

#Append Message to the db
class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"Message from {self.name} ({self.email})"
    
class Visitor(models.Model):
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255)
    visited_at = models.DateTimeField(auto_now_add=True)
    url_visited = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.ip_address} visited at {self.visited_at}"
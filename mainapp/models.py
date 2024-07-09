from django.db import models

# Create your models here.


class Posts(models.Model):

    ticker = models.CharField(max_length=100)
    description = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): # adicionar isso
        return self.ticker
        
    class Meta:  # adicionar isso
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['id']
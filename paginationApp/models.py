from django.db import models

class Post(models.Model):
    api_id = models.IntegerField(unique=True)   # The original ID from the external API
    user_id = models.IntegerField()   # ID of the user who created the post.
    title = models.CharField(max_length=300)   # Post title
    body = models.TextField()    # Full Post content

    def __str__(self):
        return self.title
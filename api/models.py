from django.db import models
from django.contrib.auth.hashers import check_password
from memento_back.minio_storage import MinioStorage

# Create your models here.

minio_storage = MinioStorage

class User(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    profilephoto = models.ImageField(upload_to='profilephoto', blank=True, storage=minio_storage)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=50)

    def __str__(self):
        return self.name

    def check_password(self, password):
        print("compare")
        print(self.password)
        print(password)
        return self.password == password

class Moment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='moments', storage=minio_storage)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
    
    
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    moment = models.ForeignKey(Moment, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

# like can be used for both moments and comments

class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    moment = models.ForeignKey(Moment, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.name + ' liked ' + self.moment.title
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'moment'], name='unique_like_moment'),
            models.UniqueConstraint(fields=['author', 'comment'], name='unique_like_comment'),
        ]

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.follower.name + ' is following ' + self.following.name

class Tag(models.Model):
    name = models.CharField(max_length=100)
    moment = models.ForeignKey(Moment, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
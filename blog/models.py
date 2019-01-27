from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from multiselectfield import MultiSelectField
from ckeditor_uploader.fields import RichTextUploadingField
from django.template.defaultfilters import slugify
import datetime
from mptt.models import MPTTModel, TreeForeignKey

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextUploadingField(external_plugin_resources=[(
                                          'youtube',
                                          '/static/blog/ckeditor_plugins/youtube/youtube/',
                                          'plugin.js',
                                          )])
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


    BRANCH_CHOICES =(('Computer','Computer Engineering'),
                    ('Electrical','Electrical Engineering'),
                    ('Civil','Civil Engineering'),
                    ('I.T','I.T Engineering'),
                    ('Mechanical','Mechanical Engineering'),
                    ('All','All'),
                        )

    YEAR_CHOICES =(('First','First Year') ,
                    ('Second','Second Year'),
                    ('Third','Third Year'),
                    ('Fourth','Fourth Year'),
                        )
    year_of_admission = MultiSelectField(max_length=25,choices=YEAR_CHOICES,default='First')

    branch = MultiSelectField(
        max_length=25,
        choices=BRANCH_CHOICES,
        default='All',
    )

    votes = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='likes')
    dislikes = models.ManyToManyField(User, related_name='dislikes')

    @property
    def total_likes(self):
        """
        Likes for the company
        :return: Integer: Likes for the company
        """

        return (self.likes.count()-self.dislikes.count())

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    likes_comment = models.ManyToManyField(User, related_name='likes_comment')
    dislikes_comment = models.ManyToManyField(User, related_name='dislikes_comment')
    

    def __str__(self):
        return str(self.content)
    @property
    def total_likes(self):
        """
        Likes for the company
        :return: Integer: Likes for the company
        """

        return (self.likes_comment.count()-self.dislikes_comment.count())
    def get_absolute_url(self):
        #return reverse('just-parent')
        return reverse('post-detail', kwargs={'pk': self.post.pk})

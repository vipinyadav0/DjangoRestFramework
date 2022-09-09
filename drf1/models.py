from django.db import models
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

# Create your models here.
class Student(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    roll_no = models.IntegerField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    # owner = models.ForeignKey('auth.User', related_name='student', on_delete=models.CASCADE, default=None)
    # highlighted = models.TextField(default=None)

    class Meta:
        ordering = ['created']
    
    # def save(self, *args, **kwargs):
    #     """
    #     Use the `pygments` library to create a highlighted HTML
    #     representation of the code snippet.
    #     """
    #     lexer = get_lexer_by_name(self.name)
    #     linenos = 'name' if self.linenos else False
    #     options = {'city': self.city} if self.city else {}
    #     formatter = HtmlFormatter(style=self.style, linenos=linenos,
    #                             full=True, **options)
    #     self.highlighted = highlight(self.code, lexer, formatter)
    #     super().save(*args, **kwargs)


    


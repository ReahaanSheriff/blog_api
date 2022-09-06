from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

# Create your models here.
class CreateBlog(models.Model):
    blog_id = models.CharField(max_length=25, primary_key = True)
    user_id_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField( auto_now_add=True)
    title = models.CharField(max_length=50)
    body = models.TextField()
    image = models.ImageField(upload_to='pics', blank=True)
    likes = models.ManyToManyField(User, related_name="liked_list", blank=True)

class Report(models.Model):
    blog_id = models.ForeignKey(CreateBlog, on_delete=models.CASCADE)
    message = models.TextField()


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "Copy paste the token to reset your password \n {}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Swift shipping application"),
         # message:
         email_plaintext_message,
         # from:
         "reahaansheriff@gmail.com",
         # to:
         [reset_password_token.user.email],
     fail_silently=False,
     )
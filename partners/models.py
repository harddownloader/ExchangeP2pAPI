from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Partner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, blank=True)
    google_doc_id = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'auth_partner'

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)  # signal used to create a object related to user instance
def create_user_partner(sender, instance, created, **kwargs):
    if created:
        Partner.objects.create(user=instance)


@receiver(post_save, sender=User)  # signal used to save a object related to user instance
def save_user_partner(sender, instance, **kwargs):
    instance.partner.save()

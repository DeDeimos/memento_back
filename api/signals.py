# signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Follow
# from .views import send_subscription_notification

# @receiver(post_save, sender=Follow)
# def send_subscription_notification_on_create(sender, instance, created, **kwargs):
#     if created:
#         send_subscription_notification(instance.follower.id, instance.following.id)

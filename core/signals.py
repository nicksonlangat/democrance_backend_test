import random
import string

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Customer, Policy, PolicyHistory


def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(characters) for _ in range(length))


User = get_user_model()


@receiver(post_save, sender=Customer)
def create_user_for_customer(sender, instance, created, **kwargs):
    if created and not instance.user:
        user = User.objects.create_user(
            email=instance.email, password=generate_random_password()
        )

        instance.user = user

        instance.save()


@receiver(post_save, sender=Policy)
def create_policy_status_history(sender, instance, created, **kwargs):
    if created:
        PolicyHistory.objects.create(
            policy=instance, status=instance.status, changed_at=timezone.now()
        )
    else:
        last_policy_history = (
            PolicyHistory.objects.filter(policy=instance)
            .order_by("-updated_at")
            .first()
        )

        if last_policy_history is None or last_policy_history.status != instance.status:
            PolicyHistory.objects.create(
                policy=instance, status=instance.status, changed_at=timezone.now()
            )

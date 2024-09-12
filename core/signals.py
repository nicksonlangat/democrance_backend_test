import random
import string

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Customer


def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(characters) for _ in range(length))


User = get_user_model()


@receiver(post_save, sender=Customer)
def create_user_for_customer(sender, instance, created, **kwargs):
    # only if the customer has no user selected

    if created and not instance.user:
        # create a user for the customer
        user = User.objects.create_user(
            email=instance.email, password=generate_random_password()
        )
        # update customer's user
        instance.user = user

        instance.save()

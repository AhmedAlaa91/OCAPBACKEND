from django.db import models


class CarManager(models.Manager):
    def get_user_cars(self, *args, **kwargs):
        """
              return cars created by user -- filter car model based on user
        """
        user = None
        for key, value in kwargs.items():
            if key == "user":
                user = value
        return super().get_queryset().filter(Owner=user)

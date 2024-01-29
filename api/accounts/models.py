from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from rest_framework_simplejwt.tokens import RefreshToken
import random


class User(AbstractUser):
    email = models.EmailField(unique = True, null= True, blank=True)
    photo =  models.ImageField( upload_to="user_photo/",
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "svg", "heic", "heif", "webp"]
            )
        ],
    )
    
    
    @property
    def full_name(self):
        return f"{self.first_name}"
    
    def token(self):
        refresh = RefreshToken.for_user(self)
        return {"access": str(refresh.access_token), "refresh": str(refresh)}
    
    
    # def create_code(self):
    #     code = "".join([str(random.randint(0, 10) % 10) for _ in range(6)])
    #     User.objects.create(
    #         user = self,
    #         code = code
    #     )
    #     return code



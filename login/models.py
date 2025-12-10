from django.db import models

class Login_Background_image(models.Model):
    image = models.ImageField(upload_to='login_images/')

    def __str__(self):
        return self.image.url
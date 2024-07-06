from django.db import models
from django.contrib.auth.models import User,AbstractBaseUser, BaseUserManager
 
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique=True, null=None, default="username")
    phone_no = models.CharField(max_length=50, unique=True, default="111111111")
    user_bio = models.TextField(max_length=100)
    user_profile_img = models.ImageField(default="media/icon/person-man.webp", upload_to="profile_img")
    address = models.TextField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    status = models.TextField(max_length=100)
    
    def __str__(self):
        return self.user.username
  

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
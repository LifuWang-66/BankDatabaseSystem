from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# # Create your models here.
# class User(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(db_column='perID', primary_key=True, max_length=100)  # Field name made lowercase.
#     pwd = models.CharField(max_length=100)

#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELD = ['username',]

#     class Meta:
#         managed = False
#         db_table = 'person'

#     def __str__(self):
#         return self.perid

#     def has_perm(self, perm, obj=None):
#         return self.is_admin
    
#     def has_module_perms(self, app_label):
#         return True
    

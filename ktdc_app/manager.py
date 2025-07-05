from django.contrib.auth.base_user import BaseUserManager



class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self,aadhar_id,password = None,**extra_fields):
        if not aadhar_id:
            raise ValueError('Aadhar id is required')

        user = self.model(aadhar_id = aadhar_id,**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,aadhar_id,password,**extra_fields):
        extra_fields.setdefault('is_staff',True) 
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        return self.create_user(aadhar_id,password,**extra_fields)

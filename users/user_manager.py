from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, **extra_fields):
        if not email:
            raise ValueError("Email is required.")
        
        extra_fields['email'] = self.normalize_email(extra_fields['email'])
        user = self.model(email=email, **extra_fields)
        user.set_unusable_password()
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, **extra_fields)
        
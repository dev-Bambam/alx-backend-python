import uuid
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

# --- Custom User Manager (Required for AbstractBaseUSer)


class CustomUserManager(BaseUserManager):
    """Custom manager for the User model where email is the unique identifier for auth instead of usernames"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", self.model.Role.Admin)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)


# --- 1. Custom User Model ---
class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model to use extending AbstractBaseUser to use email as the unique identifier and the UUID as the primary key, as required by the specification"""

    class Role(models.TextChoices):
        # Maps the ENUM requirements to Django's TextChoices for robust handling.

        GUEST = "guest", "Guest"
        HOST = "host", "Host"
        ADMIN = "admin", "Admin"

    # user_id (Primary Keys, UUID, Indexed)
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="User ID"
    )

    # email (VARCHAR, UNIQUE, NOT NULL)
    email = models.EmailField(unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)
    # password_hash is handled by AbstractBaseUser
    phone_number = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                r"^\+?1?\d{9,15}$",
                'Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.',
            )
        ],
    )

    # role (ENUM, NOT NULL, default to GUEST)
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.GUEST,
        null=False,
        blank=False
    )
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    # Required fields for AbstractBaseUser and PermissionMixin
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Set manager and authentication fields
    objects = CustomUserManager()
    USERNAME_FIELD = 'email' # use email for login
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role'] # fields asked for when creating a user

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        '''Returns the first name plus the last name with a space'''
        return f'{self.first_name} {self.last_name}'.strip()
    
    class Meta:
        verbose_name = 'User',
        verbose_name_plural = 'Users'

# 2. Conversation Model 
class Conversation(models.Model):
    '''Rep a chat conversation between multiple user'''
    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Conversation ID'
    )
    participants = models.ManyToManyField(
        User,
        related_name='conversations',
        verbose_name='Participants'
    )
    created_at = models.CharField(
        default=timezone.now,
        editable=False
    )
    title = models.CharField(
        max_length=255, blank=True, null=True
    )

    def __str__(self):
        if self.title:
            return self.title
        return f'Conversation({self.conversation_id})'
    
    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = 'Conversations'
        # Ensure that the most recent chats are listed first
        ordering = ['-created_at']

# 3. --- Message Model ---
class Message(models.Model):
    '''Rep a single message sent within a conversation'''
    message_id = models.UUIDField(
        primary_key=True,
        default= uuid.uuid4,
        editable=False,
        verbose_name='Message ID'
    )
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name='Sender'
    )
    chat = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Conversation'
    )
    message_body = models.TextField(
        null=False, 
        blank=False
    )
    sent_at = models.DateTimeField(default=timezone.now, editable=False)

    # Additional Indexing on the foreign for faster lookup
    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['sent_at']
        # Add index for fast lookup by conversation and sender
        indexes = [
            models.Index(fields=['chat', 'sent_At']),
            models.Index(fields=['sender'])
        ]

    def __str__(self):
        return f'Message from {self.sender.email} in Chat {self.chat.conversation_id}'
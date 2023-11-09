import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager


class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    gender = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(null=True, upload_to="images/users/%Y-%m-%d/")
    date_of_birth = models.DateField(
        null=True,
    )
    cityzenship = models.CharField(max_length=255, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name


class CategoryRunner(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)


class CharitableOrganization(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=255,
        null=False,
    )
    caption = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    image = models.ImageField(
        null=True, upload_to="images/charitable_organization/%Y-%m-%d/"
    )
    timestamp = models.DateTimeField(auto_now_add=True)


class Runner(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
    )
    category_runner = models.ForeignKey(
        CategoryRunner,
        on_delete=models.CASCADE,
        null=False,
    )
    timestamp = models.DateTimeField(auto_now_add=True)


class Sponsor(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    card = models.CharField(
        max_length=255,
        null=False,
    )
    number_card = models.CharField(
        max_length=255,
        null=False,
    )
    validity_period = models.DateField(
        null=False,
    )
    cvc = models.CharField(
        max_length=3,
        null=False,
    )
    timestamp = models.DateTimeField(auto_now_add=True)


class RunnerAndSponsor(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    runner = models.ForeignKey(
        Runner,
        on_delete=models.CASCADE,
        null=False,
    )
    sponsor = models.ForeignKey(
        Sponsor,
        on_delete=models.CASCADE,
        null=False,
    )
    contribution = models.DecimalField(max_digits=5, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)


class Marathon(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=255,
        null=False,
    )
    caption = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=False,
    )
    distance = models.IntegerField()
    image = models.ImageField(null=True, upload_to="images/marathon/%Y-%m-%d/")
    date = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now_add=True)


class KitOption(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)


class Inventory(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False)
    left = models.IntegerField()
    must_be = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)


class KitOptionsAndInventory(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kit_option = models.ForeignKey(
        KitOption,
        on_delete=models.CASCADE,
        null=False,
    )
    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        null=False,
    )
    timestamp = models.DateTimeField(auto_now_add=True)


class MarathonResult(models.Model):
    runner = models.ForeignKey(
        Runner,
        on_delete=models.CASCADE,
        null=False,
    )
    marathon = models.ForeignKey(
        Marathon,
        on_delete=models.CASCADE,
        null=False,
    )
    charitable_organization = models.ForeignKey(
        CharitableOrganization,
        on_delete=models.CASCADE,
        null=False,
    )
    kit_option = models.ForeignKey(
        KitOption,
        on_delete=models.CASCADE,
        null=False,
    )
    common_place = models.IntegerField(default=0)
    place_by_category = models.IntegerField(default=0)
    is_confirmed_payment = models.BooleanField(default=False)
    distance_passing_time = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

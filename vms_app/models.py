from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import models, transaction
from django.utils import timezone


class Company(models.Model):
    company_name = models.CharField(max_length=70)

    class Meta:
        ordering = ['company_name']

    def __str__(self):
        return self.company_name


class Shop(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='shops')
    location = models.CharField(max_length=100)
    address = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.company.company_name} {self.location}"


class User(AbstractUser):
    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ['username', 'email']

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='users',
        null=True
    )

    def __str__(self):
        return self.username


class Client(models.Model):
    firstname = models.CharField(max_length=70)
    lastname = models.CharField(max_length=70)
    email = models.EmailField(max_length=50)
    contact = models.CharField(max_length=20)
    logo = models.URLField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['lastname', 'firstname']

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class VoucherRequest(models.Model):
    class RequestStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PAID = 'paid', 'Paid'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'

    class Meta:
        ordering = ['request_ref']
        permissions = [
            ("reject_request", "Can reject a voucher request"),
            ("approve_request", "Can approve a voucher request"),
            ("change_to_paid", "Can change the request_status from pending to paid"),
        ]

    recorded_by = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_voucher_requests', null=True, blank=True
    )
    approved_by = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='approved_requests', null=True, blank=True
    )
    request_ref = models.TextField(unique=True, blank=True, null=True)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, null=True, blank=True,
        related_name='client_voucher_requests'
    )
    request_status = models.CharField(max_length=20, choices=RequestStatus.choices, default=RequestStatus.PENDING)
    date_time_recorded = models.DateTimeField(default=timezone.now, blank=True)
    quantity_of_vouchers = models.IntegerField(blank=False, null=False, default=1)
    description = models.TextField(blank=True, null=True)
    date_time_approved = models.DateTimeField(null=True, blank=True)

    def set_date_time_approved(self):
        """Set the approval timestamp when the request is approved."""
        self.date_time_approved = timezone.now()
        self.save()

    def clean(self):
        # retrieve request_status before update
        if self.pk:
            old_status = VoucherRequest.objects.get(pk=self.pk).request_status

            if old_status in ('approved', 'rejected') and self.request_status != old_status:
                raise ValidationError(f"Invalid status: {old_status} requests cannot modified")

            if old_status == 'pending' and self.request_status not in ('paid', 'rejected', 'pending'):
                raise ValidationError("Invalid status: pending requests can only be paid or rejected")

            if old_status == 'paid' and self.request_status not in ('paid', 'rejected', 'approved'):
                raise ValidationError("Invalid status: pending requests can only be approved or rejected")


    def __str__(self):
        return f"Voucher Request ref: {self.request_ref}"


class Voucher(models.Model):
    class VoucherStatus(models.TextChoices):
        PROVISIONAL = 'provisional', 'Provisional'
        ISSUED = 'issued', 'Issued'
        EXPIRED = 'expired', 'Expired'
        REDEEMED = 'redeemed', 'Redeemed'
        CANCELLED = 'cancelled', 'Cancelled'

    class Meta:
        ordering = ['voucher_ref']
        permissions = [("redeem_voucher", "Can redeem voucher")]

    voucher_request = models.ForeignKey(VoucherRequest, on_delete=models.CASCADE, related_name='vouchers')
    voucher_ref = models.TextField(unique=True, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_time_created = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateField(blank=False, null=False)
    extention_date = models.DateField(null=True, blank=True)
    voucher_status = models.CharField(
        max_length=20,
        choices=VoucherStatus.choices,
        default=VoucherStatus.PROVISIONAL
    )

    def redeem(self, user, shop, till_no):
        """Redeem the voucher by creating a Redemption and updating status."""
        if not user.has_perm('app_name.redeem_voucher'):
            raise PermissionDenied("You do not have permission to redeem vouchers.")

        if self.voucher_status != Voucher.VoucherStatus.ISSUED:
            raise ValueError("Voucher must be issued to be redeemed.")
        # Create the Redemption
        Redemption.objects.create(voucher=self, user=user, shop=shop, till_no=till_no)
        # Update voucher status to redeemed
        self.voucher_status = Voucher.VoucherStatus.REDEEMED
        self.save()

    def __str__(self):
        return f"Ref: {self.voucher_ref}; Amount: {self.amount} MUR"


class Redemption(models.Model):
    voucher = models.OneToOneField(
        Voucher, on_delete=models.CASCADE,
        related_name='redemption',
        null=True, blank=False
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_redemptions',
        null=False, blank=False
    )
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='shop_redemptions')
    redemption_date = models.DateTimeField(default=timezone.now)
    till_no = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return (f"voucher_ref: {self.voucher.voucher_ref}, "
            f"redeemed_on: {self.redemption_date}, "
            f"shop: {self.shop.company.company_name} {self.shop.location}")


class AuditTrails(models.Model):
    class AuditTrailsAction(models.TextChoices):
        ADD = 'add', 'Add'
        UPDATE = 'update', 'Update'
        DELETE = 'delete', 'Delete'

    class Meta:
        ordering = ['datetime']

    datetime = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_trails')
    table_name = models.CharField(max_length=20)
    object_id = models.IntegerField()
    description = models.TextField()
    action = models.CharField(
        max_length=10,
        choices=AuditTrailsAction.choices,
        null=True, blank=False
    )

    def __str__(self):
        return f"user: {self.user.username}, table_name: {self.table_name}, action: {self.action}"

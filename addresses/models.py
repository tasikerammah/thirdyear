from django.db import models
from django.shortcuts import reverse
from billing.models import BillingProfile

ADDRESS_TYPES = (
    ('derivary', 'Delivery address'),
    ('pick', 'In person Pick'),
)

class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    name            = models.CharField(max_length=120, null=True, blank=True, help_text='Derivaring to? Who is it for?')
    nickname        = models.CharField(max_length=120, null=True, blank=True, help_text='Internal Reference Nickname')
    address_type    = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    residence         = models.CharField(max_length=120, default="Hostel K")
    phone_number    = models.CharField(max_length=50)

    def __str__(self):
        if self.nickname:
            return str(self.nickname)
        return str(self.address_line)

    def get_absolute_url(self):
        return reverse("address-update", kwargs={"pk": self.pk})

    def get_short_address(self):
        for_name = self.name 
        if self.nickname:
            for_name = "{} | {},".format( self.nickname, for_name)
        return "{for_name} {line1}, {residence}".format(
                for_name = for_name or "",
                line1 = self.address_line,
                residence = self.residence
            ) 

    def get_address(self):
        return "{for_name}\n{line1}\n{residence}\n{phone}".format(
                for_name = self.name or "",
                line1 = self.address_line or '',
                residence = self.residence,
                phone = self.phone_number
            )

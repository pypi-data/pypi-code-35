from django.db import models
from django.utils.translation import gettext as _


class ContactInformation(models.Model):
    """
    This model will store the comapny places to be shown in a contact page
    """

    name = models.CharField(_('nombre'), max_length=255)
    address = models.TextField(_('dirección'))
    phone_number = models.CharField(
        _('teléfono'),
        max_length=255,
        help_text="Si hay me de uno, separar con comas"
    )
    email = models.EmailField(_('email'))
    latitude = models.DecimalField(_('latitud'), max_digits=11, decimal_places=8)
    longitude = models.DecimalField(_('longitud'), max_digits=11, decimal_places=8)

    class Meta:
        verbose_name = _("Información de contacto")
        verbose_name_plural = _("Informaciones de contacto")

    def __str__(self):
        return self.name

    def get_phone_number(self):
        """
        Returns the phone_number in a list form.
        """
        return [phone.strip() for phone in self.phone_number.split(',')]


class ContactRequest(models.Model):
    """
    This model will manage the requests from the contact form
    """

    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    name = models.CharField(_('nombre'), max_length=255)
    email = models.EmailField(_('email'))
    phone_number = models.CharField(_('teléfono'), max_length=255)
    message = models.TextField(_('mensaje'))
    contacted = models.BooleanField(_('contactado'), default=False)

    class Meta:
        verbose_name = _("Petición de contacto")
        verbose_name_plural = _("Peticiones de contacto")

    def __str__(self):
        return self.name

    @property
    def contact_information(self):
        if self.email and self.phone_number:
            return _("{email} o {phone_number}").format(
                email=self.email,
                phone_number=self.phone_number
            )
        if self.email:
            return self.email
        return self.phone_number

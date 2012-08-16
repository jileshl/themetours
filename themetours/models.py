import json
from django.db import models

class Service(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=15)
    code = models.CharField(max_length=3)
    service_tax = models.DecimalField(max_digits=5, decimal_places=2)
    education_cess = models.DecimalField(max_digits=5, decimal_places=2)
    higher_secondary = models.DecimalField(max_digits=5, decimal_places=2)
    from_date = models.DateField(blank=False)
    to_date = models.DateField(null=True)

    # ....
    def to_json(self):
        return json.dumps([str(self.id), str(self.id), self.name, self.code, str(self.service_tax), str(self.education_cess), str(self.higher_secondary), str(self.from_date), str(self.to_date)])

    def get_query_set(self):
        return super(Service, self).get_query_set().filter(is_deleted=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "service"
        verbose_name_plural = "services"

class Client(models.Model):
    SALUATION_MAP = (
        ('Mr', 'Mr.'),
        ('Ms', 'Ms.'),
        ('Mrs', 'Mrs.'),
        ('Smt', 'Smt.'),
        ('Shri', 'Shri '),
        ('Mast', 'Mast.'),
        ('Miss', 'Miss.'),
        ('Dr', 'Dr.'),
        ('Prof', 'Prof.'),
        (' ', ' '),
    )

    id = models.AutoField(primary_key=True)
    saluation = models.CharField(max_length=7, choices=SALUATION_MAP)
    company = models.CharField(max_length=150, blank=True)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    address_line1 = models.CharField(max_length=250)
    address_line2 = models.CharField(max_length=250)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=75)
    zip = models.BigIntegerField(max_length=7)
    country = models.CharField(max_length=30)
    contact_phone = models.BigIntegerField(max_length=13)
    email = models.EmailField(max_length=75)
    pan_no = models.CharField(max_length=15)
    reference_name = models.CharField(max_length=200)
    is_deleted = models.BooleanField(default=False)

    def get_query_set(self):
        return super(Client, self).get_query_set().filter(is_deleted=False)

    def _get_full_name(self):
        return '%s %s %s' % (self.saluation, self.first_name, self.last_name)
    full_name = property(_get_full_name)

    def _get_display_name(self):
        if None == self.company or 0 == len(self.company):
            return self.full_name
        else:
            return self.company
    display_name = property(_get_display_name)

    def to_json(self):
        return json.dumps([str(self.id), str(self.id), self.company, self.display_name, self.city, self.contact_phone, self.email, self.reference_name])

    class Meta:
        verbose_name = "client"
        verbose_name_plural = "clients"

    # ...
    def __unicode__(self):
        return self.display_name

class Supplier(models.Model):
    SALUATION_MAP = (
        ('Mr', 'Mr.'),
        ('Ms', 'Ms.'),
        ('Mrs', 'Mrs.'),
        ('Smt', 'Smt.'),
        ('Shri', 'Shri '),
        ('Mast', 'Mast.'),
        ('Miss', 'Miss.'),
        ('Dr', 'Dr.'),
        ('Prof', 'Prof.'),
        (' ', ' '),
    )

    id = models.AutoField(primary_key=True)
    service_type = models.ForeignKey(Service)
    company = models.CharField(max_length=150, blank=True)
    saluation = models.CharField(max_length=6, choices=SALUATION_MAP)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=500)
    address_line1 = models.CharField(max_length=250)
    address_line2 = models.CharField(max_length=250)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=75)
    zip = models.BigIntegerField(max_length=7)
    country = models.CharField(max_length=30)
    contact_phone = models.BigIntegerField(max_length=13)
    email = models.EmailField(max_length=75)
    pan_no = models.CharField(max_length=15, blank=True)
    service_reg_no = models.CharField(max_length=20, blank=True)
    is_deleted = models.BooleanField(default=False)

    def _get_full_name(self):
        return '%s %s %s' % (self.saluation, self.first_name, self.last_name)
    full_name = property(_get_full_name)

    def _get_display_name(self):
        if None == self.company or 0 == len(self.company):
            return self.full_name
        else:
            return self.company
    display_name = property(_get_display_name)

    def to_json(self):
        return json.dumps([str(self.id), str(self.id), self.service_type.code, self.company, self.full_name, self.city, self.contact_phone, self.email])

    def get_query_set(self):
        return super(Supplier, self).get_query_set().filter(is_deleted=False)

    # ...
    def __unicode__(self):
        return self.display_name

    class Meta:
        verbose_name = "supplier"
        verbose_name_plural = "suppliers"

class Sale(models.Model):
    id = models.AutoField(primary_key=True)
    service_type = models.ForeignKey(Service)
    client = models.ForeignKey(Client)
    sales_transaction_no = models.CharField(max_length=25, blank=True)
    sales_date = models.DateField();
    service_tax = models.DecimalField(max_digits=19, decimal_places=2)
    education_cess = models.DecimalField(max_digits=19, decimal_places=2)
    higher_secondary = models.DecimalField(max_digits=19, decimal_places=2)
    additional_service_charge = models.DecimalField(max_digits=19, decimal_places=2)
    discount = models.DecimalField(max_digits=19, decimal_places=2)
    round_off = models.DecimalField(max_digits=19, decimal_places=2)
    total = models.DecimalField(max_digits=19, decimal_places=2, blank=True)
    when_date =  models.DateTimeField(auto_now = True, auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def to_json(self):
        return json.dumps([str(self.id), str(self.id), self.service_type.code, self.client.display_name, self.sales_transaction_no, str(self.id)])

    def get_query_set(self):
        return super(Sale, self).get_query_set().filter(is_deleted=False)

    def save(self, *args, **kwargs):
        super(Sale, self).save(*args, **kwargs) # Call the "real" save() method.
        self.sales_transaction_no = self.service_type.code+ '/'+ str(self.id)
        super(Sale, self).save(*args, **kwargs) # Call the "real" save() method.

    # ...
    def __unicode__(self):
        return str(self.id)

    class Meta:
        verbose_name = "sale"
        verbose_name_plural = "sales"

class Purchase(models.Model):
    id = models.AutoField(primary_key=True)
    sales = models.ForeignKey(Sale)
    purchase_transaction_no = models.CharField(max_length=25, blank=True)
    supplier = models.ForeignKey(Supplier)
    service_tax = models.DecimalField(max_digits=19, decimal_places=2, blank=True)
    education_cess = models.DecimalField(max_digits=19, decimal_places=2, blank=True)
    higher_secondary = models.DecimalField(max_digits=19, decimal_places=2, blank=True)
    tds = models.DecimalField(max_digits=19, decimal_places=2, blank=True)
    discount = models.DecimalField(max_digits=19, decimal_places=2, blank=True)
    round_off = models.DecimalField(max_digits=19, decimal_places=2, blank=True)
    when_date =  models.DateTimeField(auto_now = True, auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=19, decimal_places=2, blank=True)

    # ...
    def __unicode__(self):
        return str(self.id)

    def get_query_set(self):
        return super(Purchase, self).get_query_set().filter(is_deleted=False)

    def save(self, *args, **kwargs):
        super(Purchase, self).save(*args, **kwargs) # Call the "real" save() method.
        self.purchase_transaction_no = 'P/' +self.sales.service_type.code+ '/'+ str(self.id)
        super(Purchase, self).save(*args, **kwargs) # Call the "real" save() method.

    def to_json(self):
        return json.dumps([self.id, self.id, self.purchase_transaction_no, self.supplier.company, str(self.service_tax), str(self.education_cess), str(self.higher_secondary), str(self.tds), str(self.discount)])
    class Meta:
        verbose_name = "purchase"
        verbose_name_plural = "purchasers"

class PassengerInfo(models.Model):
    id = models.AutoField(primary_key=True)
    when_date =  models.DateTimeField(auto_now = True, auto_now_add=True)
    sales_transaction_no = models.ForeignKey(Sale)
    purchase_transaction_no = models.ForeignKey(Purchase)
    supplier = models.ForeignKey(Supplier)
    pax_name = models.CharField(max_length=150)
    transaction_no = models.CharField(max_length = 30)

    sector_from1 = models.CharField(max_length=5)
    sector_to1 = models.CharField(max_length=5)
    travel_date1 = models.DateField()

    sector_from2 = models.CharField(max_length=5, blank=True, null=True)
    sector_to2 = models.CharField(max_length=5, blank=True, null=True)
    travel_date2 = models.DateField(blank=True, null=True)

    sector_from3 = models.CharField(max_length=5, blank=True, null=True)
    sector_to3 = models.CharField(max_length=5, blank=True, null=True)
    travel_date3 = models.DateField(blank=True, null=True)

    sector_from4 = models.CharField(max_length=5, blank=True, null=True)
    sector_to4 = models.CharField(max_length=5, blank=True, null=True)
    travel_date4 = models.DateField(blank=True, null=True)

    sector_from5 = models.CharField(max_length=5, blank=True, null=True)
    sector_to5 = models.CharField(max_length=5, blank=True, null=True)
    travel_date5 = models.DateField(blank=True, null=True)

    sector_from6 = models.CharField(max_length=5, blank=True, null=True)
    sector_to6 = models.CharField(max_length=5, blank=True, null=True)
    travel_date6 = models.DateField(blank=True, null=True)

    basic_fare = models.DecimalField(max_digits=19, decimal_places=2)
    airline_taxes = models.DecimalField(max_digits=19, decimal_places=2)
    is_deleted = models.BooleanField(default=False)

    # ...
    def __unicode__(self):
        return str(self.id)

    class Meta:
        verbose_name = "passenger_info"
        verbose_name_plural = "passenger_infos"

class creditNote(models.Model):
    id = models.AutoField(primary_key=True)
    passenger = models.ForeignKey(PassengerInfo)
    service_tax = models.DecimalField(max_digits=19, decimal_places=2)
    education_cess = models.DecimalField(max_digits=19, decimal_places=2)
    higher_secondary = models.DecimalField(max_digits=19, decimal_places=2)
    additional_service_charge = models.DecimalField(max_digits=19, decimal_places=2)
    discount = models.DecimalField(max_digits=19, decimal_places=2)
    round_off = models.DecimalField(max_digits=19, decimal_places=2)
    is_deleted = models.BooleanField(default=False)

    # ...
    def __unicode__(self):
        return str(self.id)

    def get_query_set(self):
        return super(creditNote, self).get_query_set().filter(is_deleted=False)

    class Meta:
        verbose_name = "credit_note"
        verbose_name_plural = "credit_notes"


class debitNote(models.Model):
    id = models.AutoField(primary_key=True)
    passenger = models.ForeignKey(PassengerInfo)
    service_tax = models.DecimalField(max_digits=19, decimal_places=2)
    education_cess = models.DecimalField(max_digits=19, decimal_places=2)
    higher_secondary = models.DecimalField(max_digits=19, decimal_places=2)
    additional_service_charge = models.DecimalField(max_digits=19, decimal_places=2)
    discount = models.DecimalField(max_digits=19, decimal_places=2)
    round_off = models.DecimalField(max_digits=19, decimal_places=2)
    is_deleted = models.BooleanField(default=False)

    # ...
    def __unicode__(self):
        return str(self.id)

    def get_query_set(self):
        return super(debitNote, self).get_query_set().filter(is_deleted=False)

    class Meta:
        verbose_name = "debit_info"
        verbose_name_plural = "debit_infos"

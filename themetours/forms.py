from django import forms
from django.forms import ModelForm
from themetours.models import Client, Supplier, Purchase, Service, Sale, PassengerInfo, creditNote, debitNote
from django.forms.extras import SelectDateWidget
import datetime

class ServiceForm(ModelForm):
      class Meta:
            model = Service

class ClientForm(ModelForm):
      class Meta:
            model = Client
            exclude = ('is_deleted');

class SupplierForm(ModelForm):
      class Meta:
            model = Supplier
            exclude = ('is_deleted');

class PassengerInfoForm(ModelForm):
      supplier = forms.ModelChoiceField(label="Supplier", queryset=Supplier.objects.filter(service_type__id=Service.objects.filter()[0].id, is_deleted=False))
      pax_name = forms.CharField(label="Passanger Name", max_length=120, widget=forms.TextInput(attrs={"size":"70"}))
      transaction_no = forms.CharField(label="Txn # / Booking #", max_length=16, widget=forms.TextInput)

      sector_from1 = forms.CharField(label="From", max_length=3, widget=forms.TextInput(attrs={"size":"4"}))
      sector_to1 = forms.CharField(label="To", max_length=3, widget=forms.TextInput(attrs={"size":"4"}))
      travel_date1 =  forms.DateField(label="Date", initial=datetime.date.today, widget=SelectDateWidget())

      sector_from2 = forms.CharField(label="From", max_length=3, required=False, widget=forms.TextInput(attrs={"size":"4"}))
      sector_to2 = forms.CharField(label="To", max_length=3, required=False, widget=forms.TextInput(attrs={"size":"4"}))
      travel_date2 =  forms.DateField(label="Date", required=False, initial=datetime.date.today, widget=SelectDateWidget())

      sector_from3 = forms.CharField(label="From", max_length=3, required=False, widget=forms.TextInput(attrs={"size":"4"}))
      sector_to3 = forms.CharField(label="To", max_length=3, required=False, widget=forms.TextInput(attrs={"size":"4"}))
      travel_date3 =  forms.DateField(label="Date", required=False, initial=datetime.date.today, widget=SelectDateWidget())

      sector_from4 = forms.CharField(label="From", max_length=3, required=False, widget=forms.TextInput(attrs={"size":"4"}))
      sector_to4 = forms.CharField(label="To", max_length=3, required=False, widget=forms.TextInput(attrs={"size":"4"}))
      travel_date4 =  forms.DateField(label="Date", required=False, initial=datetime.date.today, widget=SelectDateWidget())

      sector_from5 = forms.CharField(label="From", max_length=3, required=False, widget=forms.TextInput(attrs={"size":"4"}))
      sector_to5 = forms.CharField(label="To", max_length=3, required=False, widget=forms.TextInput(attrs={"size":"4"}))
      travel_date5 =  forms.DateField(label="Date", required=False, initial=datetime.date.today, widget=SelectDateWidget())

      sector_from6 = forms.CharField(label="From", max_length=3, required=False, widget=forms.TextInput(attrs={"size":"4"}))
      sector_to6 = forms.CharField(label="To", max_length=3, required=False, widget=forms.TextInput(attrs={"size":"4"}))
      travel_date6 =  forms.DateField(label="Date", required=False, initial=datetime.date.today, widget=SelectDateWidget())

      basic_fare = forms.DecimalField(label="Basic Fare",  initial=0, max_digits=19, decimal_places=2, widget=forms.TextInput(attrs={"onchange":"calculateTotal('form')"}))
      airline_taxes = forms.DecimalField(label="Airline Tax",  initial=0, max_digits=19, decimal_places=2, widget=forms.TextInput(attrs={"onchange":"calculateTotal('form')"}))

      class Meta:
            model = PassengerInfo
            exclude = ('when_date', 'sales_transaction_no', 'purchase_transaction_no', 'is_deleted',)
            fields = ('supplier', 'transaction_no',  'pax_name', 'sector_from1', 'sector_to1', 'travel_date1', 'sector_from2', 'sector_to2', 'travel_date2', 'sector_from3', 'sector_to3', 'travel_date3', 'sector_from4', 'sector_to4', 'travel_date4', 'sector_from5', 'sector_to5', 'travel_date5', 'sector_from6', 'sector_to6', 'travel_date6', 'basic_fare', 'airline_taxes')


class SaleForm(ModelForm):
      sales_date = forms.DateField(label="Date", initial=datetime.date.today, widget=forms.DateInput(format='%Y-%m-%d', attrs={'class':'datePicker', 'readonly':'true'}))
      service_type = forms.ModelChoiceField(label = "Service Type", queryset=Service.objects.all(), empty_label=None)
      client = forms.ModelChoiceField(label= "Client", queryset=Client.objects.all(), empty_label=None)
      additional_service_charge = forms.DecimalField(label="Additional Service Charges",  initial=0, max_digits=19, decimal_places=2)
      discount = forms.DecimalField(label="Discount",  initial=0, max_digits=19, decimal_places=2)
      round_off = forms.DecimalField(label="Round Off", initial=0, max_digits=19, decimal_places=2)

      service_tax_per = forms.DecimalField(label="Service Tax%", max_digits=4, decimal_places=2, widget=forms.HiddenInput)
      service_tax = forms.DecimalField(label="Service Tax", max_digits=19, decimal_places=2, widget=forms.HiddenInput)

      education_cess_per = forms.DecimalField(label="Education Cess %", max_digits=4, decimal_places=2, widget=forms.HiddenInput)
      education_cess = forms.DecimalField(label="Education Cess", max_digits=19, decimal_places=2, widget=forms.HiddenInput)

      higher_secondary_per = forms.DecimalField(label="H.C %", max_digits=4, decimal_places=2, widget=forms.HiddenInput)
      higher_secondary = forms.DecimalField(label="H.C", max_digits=19, decimal_places=2, widget=forms.HiddenInput)
      total = forms.DecimalField(label="Total", max_digits=19, decimal_places=2, initial='0.0', widget=forms.TextInput(attrs={'readonly':'readonly'}))

      class Meta:
            model = Sale
            exclude = ('sales_transaction_no')

class PurchaseForm(ModelForm):
      supplier = forms.ModelChoiceField(label="Supplier", queryset=Supplier.objects.filter(is_deleted=False))
      purchase_transaction_no = forms.CharField(label="Purcahse Txn No", max_length=25, widget=forms.HiddenInput)
      service_tax = forms.DecimalField(label="Service Tax", max_digits=19, decimal_places=2)
      education_cess = forms.DecimalField(label="Education Cess", max_digits=19, decimal_places=2)
      higher_secondary = forms.DecimalField(label="H.C", max_digits=19, decimal_places=2)
      tds = forms.DecimalField(label="tds", max_digits=19, decimal_places=2)
      discount = forms.DecimalField(label="discount", max_digits=19, decimal_places=2)
      round_off = forms.DecimalField(label="round_off", max_digits=19, decimal_places=2)
      total = forms.DecimalField(label="Total", max_digits=19, decimal_places=2, initial='0.0', widget=forms.TextInput(attrs={'readonly':'readonly'}))

      class Meta:
            model = Purchase
            exclude = ('sales','is_deleted' )

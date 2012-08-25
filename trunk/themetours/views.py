import logging
from django.core.serializers.json import DjangoJSONEncoder
from themetours.utils import get_datatables_records
from django.shortcuts import render_to_response, get_object_or_404, render
from django import http
from django.http import HttpResponse
from django.core.context_processors import csrf

from django.utils import simplejson as json
from django.core import serializers
from django.forms.models import model_to_dict, modelformset_factory, BaseModelFormSet

from django.forms import formsets
from django.forms.formsets import formset_factory, BaseFormSet

from themetours.forms import ServiceForm, ClientForm, SupplierForm, SaleForm, PurchaseForm, PassengerInfoForm
from themetours.models import Client, Supplier, Purchase, Service, Sale, PassengerInfo, creditNote, debitNote

logger = logging.getLogger(__name__)
def index(request):
    return render_to_response('themetours/index.html')
################################SERVICES####################################################
def json_services(request):
    services = Service.objects.all()

    if not 'sEcho' in request.GET or not request.GET['sEcho']:
        sEcho = '0' #default value
    else:
        sEcho = request.GET['sEcho'] #this is required by datatables

    iTotalRecords = services.count()

    if not 'iTotalDisplayRecords' in request.GET or not request.GET['iTotalDisplayRecords']:
        iTotalDisplayRecords = '10' #default value
    else:
        iTotalDisplayRecords = request.GET['iTotalDisplayRecords'] #this is required by datatables

    aaData = []
    for model in services:
        aaData.append([model.id, model.id, model.name, model.code, str(model.service_tax), str(model.education_cess), str(model.higher_secondary), str(model.from_date), str(model.to_date)])

    dict = {'sEcho': sEcho,
            'iTotalRecords': iTotalRecords,
            'iTotalDisplayRecords': iTotalDisplayRecords,
            'aaData' : aaData}

    return HttpResponse(json.dumps(dict), content_type='application/json')

def update_service(request, id):
    if 'POST' == request.method:
        if ('-1' == id):
            form = ServiceForm(request.POST)
        else:
            form = ServiceForm(request.POST, instance=Service.objects.get(id=id))

        if form.is_valid():
            model = form.save();
            return HttpResponse(model.to_json(), content_type='application/json', status=200)

        else:
            return render(request, 'themetours/update_services.html', {'form' : form, 'id' : id}, status=302)
    else:
        if '-1' == id:
            form = ServiceForm()
        else:
            form = ServiceForm(instance=Service.objects.get(id=id))

    return render(request, 'themetours/update_services.html', {'form' : form, 'id' : id})


def delete_service(request):
    if 'POST' == request.method:
        deletedIds = []

        for id in request.POST.getlist('check'):
            serviceModel = Service.objects.get(id=id)
            deletedIds.append(serviceModel.id)
            serviceModel.delete()


        return HttpResponse(json.dumps(deletedIds), content_type='application/json')

def services(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'themetours/services.html', c)

################################ CLIENTS ####################################################
def json_clients(request):
    clients = Client.objects.filter(is_deleted=False)

    if not 'sEcho' in request.GET or not request.GET['sEcho']:
        sEcho = '0' #default value
    else:
        sEcho = request.GET['sEcho'] #this is required by datatables

    iTotalRecords = clients.count()

    if not 'iTotalDisplayRecords' in request.GET or not request.GET['iTotalDisplayRecords']:
        iTotalDisplayRecords = '25' #default value
    else:
        iTotalDisplayRecords = request.GET['iTotalDisplayRecords'] #this is required by datatables

    aaData = []
    for model in clients:
        aaData.append([str(model.id), str(model.id), model.company, model.full_name, model.city, model.contact_phone, model.email, model.reference_name])

    dict = {'sEcho': sEcho,
            'iTotalRecords': iTotalRecords,
            'iTotalDisplayRecords': iTotalDisplayRecords,
            'aaData' : aaData}

    return HttpResponse(json.dumps(dict), content_type='application/json')

def update_client(request, id):
    if 'POST' == request.method:
        if ('-1' == id):
            form = ClientForm(request.POST)
        else:
            form = ClientForm(request.POST, instance=Client.objects.get(id=id))

        if form.is_valid():
            model = form.save();
            return HttpResponse(model.to_json(), content_type='application/json', status=200)

        else:
            return render(request, 'themetours/update_clients.html', {'form' : form, 'id' : id})
    else:
        if '-1' == id:
            form = ClientForm()
        else:
            form = ClientForm(instance=Client.objects.get(id=id))

    return render(request, 'themetours/update_clients.html', {'form' : form, 'id' : id})

def delete_client(request):
    if 'POST' == request.method:
        deletedIds = []

        for id in request.POST.getlist('check'):
            clientModel = Client.objects.get(id=id)
            clientModel.is_deleted = True
            clientModel.save()
            deletedIds.append(id)

        return HttpResponse(json.dumps(deletedIds), content_type='application/json')

def clients(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'themetours/clients.html', c)

############################### SUPPLIERS ####################################################

def json_suppliers(request):
    suppliers = Supplier.objects.filter(is_deleted=False)

    if not 'sEcho' in request.GET or not request.GET['sEcho']:
        sEcho = '0' #default value
    else:
        sEcho = request.GET['sEcho'] #this is required by datatables

    iTotalRecords = suppliers.count()

    if not 'iTotalDisplayRecords' in request.GET or not request.GET['iTotalDisplayRecords']:
        iTotalDisplayRecords = '25' #default value
    else:
        iTotalDisplayRecords = request.GET['iTotalDisplayRecords'] #this is required by datatables

    aaData = []
    for model in suppliers:
        aaData.append([str(model.id), str(model.id), model.service_type.name, model.company, model.full_name, model.city, model.contact_phone, model.email])

    dict = {'sEcho': sEcho,
            'iTotalRecords': iTotalRecords,
            'iTotalDisplayRecords': iTotalDisplayRecords,
            'aaData' : aaData}

    return HttpResponse(json.dumps(dict), content_type='application/json')

def update_supplier(request, id):
    if 'POST' == request.method:
        if ('-1' == id):
            form = SupplierForm(request.POST)
        else:
            form = SupplierForm(request.POST, instance=Supplier.objects.get(id=id))

        if form.is_valid():
            model = form.save();
            return HttpResponse(model.to_json(), content_type='application/json', status=200)

        else:
            return render(request, 'themetours/update_suppliers.html', {'form' : form, 'id' : id}, status=302)
    else:
        if '-1' == id:
            form = SupplierForm()
        else:
            form = SupplierForm(instance=Supplier.objects.get(id=id))

    return render(request, 'themetours/update_suppliers.html', {'form' : form, 'id' : id})

def delete_supplier(request):
    if 'POST' == request.method:
        deletedIds = []

        for id in request.POST.getlist('check'):
            supplierModel = Supplier.objects.get(id=id)
            supplierModel.is_deleted = True
            supplierModel.save()
            deletedIds.append(id)

        return HttpResponse(json.dumps(deletedIds), content_type='application/json')

def suppliers(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'themetours/suppliers.html', c)

############################################################ SALES ####################################################################################

def sales(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'themetours/airsales.html', c)

def json_sales(request):
    sales = Sale.objects.filter(is_deleted=False)

    if not 'sEcho' in request.GET or not request.GET['sEcho']:
        sEcho = '0' #default value
    else:
        sEcho = request.GET['sEcho'] #this is required by datatables

    iTotalRecords = sales.count()

    if not 'iTotalDisplayRecords' in request.GET or not request.GET['iTotalDisplayRecords']:
        iTotalDisplayRecords = '10' #default value
    else:
        iTotalDisplayRecords = request.GET['iTotalDisplayRecords'] #this is required by datatables

    aaData = []
    for model in sales:
        aaData.append([str(model.id), str(model.id), model.service_type.code, model.client.display_name, model.sales_transaction_no, str(model.id)])

    dict = {'sEcho': sEcho,
            'iTotalRecords': iTotalRecords,
            'iTotalDisplayRecords': iTotalDisplayRecords,
            'aaData' : aaData}

    return HttpResponse(json.dumps(dict), content_type='application/json')

class PassengerInfoFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(PassengerInfoFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = True

def update_airsale(request, id):
    PassengerFormSet = modelformset_factory(PassengerInfo,
                                            formset=PassengerInfoFormSet,
                                            can_delete=False,
                                            can_order=False,
                                            max_num=6,
                                            extra=0,
                                            form=PassengerInfoForm,
                                            exclude = ('date',
                                                       'is_deleted',
                                                       'sales_transaction_no',
                                                       'purchase_transaction_no')
                                            )
    if 'POST' == request.method:
        if ('-1' == id):
            salesForm = SaleForm(request.POST, prefix='s')
            passenger_info_formset = PassengerFormSet(request.POST)

        else:
            salesForm = SaleForm(request.POST, instance=Sale.objects.get(id=id, is_deleted=False), prefix='s')
            passenger_info_formset = PassengerFormSet(request.POST)

        if salesForm.is_valid() and passenger_info_formset.is_valid():
            salesModel = salesForm.save(commit=False)
            salesModel.sales_transaction_no = salesModel.service_type.name+ '/'+ str(salesModel.id)

            airpassengerInfo_ids = []
            for form in passenger_info_formset.forms:
                try:
                    passenger_info = form.save(commit=False)
                except e:
                    raise form.ValidationError(e.__str__)

                if passenger_info.id is not None:
                    airpassengerInfo_ids.append(passenger_info.id)

                deletedModels = PassengerInfo.objects.filter(sales_transaction_no=salesModel).exclude(id__in=airpassengerInfo_ids)
                for dPmodels in deletedModels:
                    dPmodels.is_deleted = True;
                    dPmodels.save()

                try:
                    purchaseModel = Purchase.objects.get(supplier=passenger_info.supplier, sales=salesModel, is_deleted=False)
                except:
                    purchaseModel = Purchase(supplier=passenger_info.supplier, sales=salesModel)
                    purchaseModel.purchase_transaction_no = 'P/' +salesModel.service_type.name+ '/'+ str(purchaseModel.id)
                    purchaseModel.service_tax = 0.0
                    purchaseModel.education_cess = 0.0
                    purchaseModel.higher_secondary = 0.0
                    purchaseModel.tds = 0
                    purchaseModel.discount = 0
                    purchaseModel.round_off = 0
                    purchaseModel.total = 0.0

                if (None !=  purchaseModel):
                    purchaseModel.supplier = passenger_info.supplier
                    purchaseModel.service_tax = 0.0
                    purchaseModel.education_cess = 0.0
                    purchaseModel.higher_secondary = 0.0
                    purchaseModel.tds = 0
                    purchaseModel.discount = 0
                    purchaseModel.round_off = 0
                    purchaseModel.total = 0.0

                purchaseForm = PurchaseForm(instance=purchaseModel)
                pmodel = purchaseForm.save(commit=False)

                try:
                    passenger_info.purchase_transaction_no = pmodel
                    passenger_info.sales_transaction_no = salesModel
                    form.save_m2m()

                    salesModel.save()
                    salesModel.sales_transaction_no = salesModel.service_type.code+'/'+str(salesModel.id)
                    salesModel.save()

                    purchaseModel.sales = salesModel
                    purchaseModel.save()

                    purchaseModel.purchase_transaction_no = 'P-'+purchaseModel.sales.service_type.code+'/'+str(purchaseModel.id)
                    purchaseModel.save()

                    passenger_info.purchase_transaction_no = purchaseModel
                    passenger_info.sales_transaction_no = salesModel
                    passenger_info.save()

                except ValueError as e:
                    raise form.ValidationError(e.__str__)

            return HttpResponse(salesModel.to_json(), content_type='application/json', status=200)

        else:
            return render(request, 'themetours/update_airsales.html', {'formset' : passenger_info_formset,
                                                                       'salesForm' : salesForm,
                                                                      'id' : id},
                          status=302)
    else:
        if '-1' == id:
            service = Service.objects.all()[0]
            salesForm = SaleForm(prefix='s', initial={'service_tax_per':service.service_tax, 'education_cess_per': service.education_cess, 'higher_secondary_per':service.higher_secondary})
            PassengerFormSet = modelformset_factory(PassengerInfo,
                                                    formset=PassengerInfoFormSet,
                                                    can_delete=False,
                                                    can_order=False,
                                                    max_num=6,
                                                    extra=1,
                                                    form=PassengerInfoForm,
                                                    exclude = ('date',
                                                               'sales_transaction_no',
                                                               'purchase_transaction_no',
                                                               'is_deleted',
                                                               'sales_transaction_no',
                                                               'purchase_transaction_no')
                                                    )
            passenger_info_formset = PassengerFormSet(queryset=PassengerInfo.objects.none())

        else:
            saleModel = Sale.objects.get(id=id)
            service = Service.objects.get(id=saleModel.service_type.id)

            salesForm = SaleForm(instance=saleModel, prefix='s', initial={'service_tax_per':service.service_tax, 'education_cess_per': service.education_cess, 'higher_secondary_per': service.higher_secondary})
            passenger_info_formset = PassengerFormSet(queryset=PassengerInfo.objects.filter(sales_transaction_no = id, is_deleted=False))

    return render(request, 'themetours/update_airsales.html', {'salesForm' : salesForm,
                                                               'formset': passenger_info_formset, 'id' : id})

def delete_airsales(request):
    if 'POST' == request.method:
        deletedIds = []

        for id in request.POST.getlist('check'):
            salesModel = Sale.objects.get(id=id)
            passengerInfo = PassengerInfo.objects.filter(sales_transaction_no=salesModel, is_deleted=False)

            purchaseModels = []
            for passengerModel in passengerInfo:
                purchcase_models = Purchase.objects.filter(id=passengerModel.purchase_transaction_no.id, is_deleted=False)
                purchaseModels.append(purchcase_models)

                passengerModel.is_deleted=True
                passengerModel.save()

            for purchaseModel in purchaseModels:
                purchaseModel.is_deleted=True
                purchaseModel.save()

            salesModel.is_deleted = True
            salesModel.save()
            deletedIds.append(id)

        return HttpResponse(json.dumps(deletedIds), content_type='application/json')

def service_related_models(request, id):
    service_model = Service.objects.filter(id=id)
    supplier_info = Supplier.objects.filter(service_type__id=id, is_deleted=False)

    return HttpResponse(serializers.serialize('json', list(service_model) + list(supplier_info)), content_type='application/json')

####################################################PURCHASE#########################################################################

class PassengerInfoFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(PassengerInfoFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = True

def update_saleairpurchase(request, saleId):
    PurchaseFormSet = modelformset_factory(Purchase, form=PurchaseForm, can_delete=False, can_order=False,extra=0)

    if request.method == 'GET':
        passenger_info = PassengerInfo.objects.filter(is_deleted=False, sales_transaction_no=(Sale.objects.get(id=saleId)))
        purchaseFormIds = [];
        for ticket in passenger_info:
            purchaseFormIds.append(ticket.purchase_transaction_no.id)

        PurchaseFormSet = modelformset_factory(Purchase, form=PurchaseForm, can_delete=False, can_order=False,extra=0)
        purchase_formset = PurchaseFormSet(queryset=Purchase.objects.filter(id__in=purchaseFormIds))

        return render(request, 'themetours/update_saleairpurchase.html', {'purchaseForm' : purchase_formset,
                                                                          'id' : id})
    else:
        purchase_formset = PurchaseFormSet(request.POST)

        if purchase_formset.is_valid():
            for form in purchase_formset:
                model = form.save()
                model.save();
        else:
            return render(request, 'themetours/update_saleairpurchase.html', {'purchaseForm' : purchase_formset,
                                                                              'id' : id},
                          status=302)
    return HttpResponse(model.to_json(), content_type='application/json')

def update_airpurchases(request, id):
    if 'POST' == request.method:
        if ('-1' == id):
            form = PurchaseForm(request.POST)
        else:
            form = PurchaseForm(request.POST, instance=Purchase.objects.get(id=id))

        if form.is_valid():
            model = form.save();
            return HttpResponse(model.to_json(), content_type='application/json', status=200)

        else:
            return render(request, 'themetours/update_airpurchase.html', {'form' : form, 'id' : id}, status=302)
    else:
        if '-1' == id:
            form = PurchaseForm()
        else:
            form = PurchaseForm(instance=Purchase.objects.get(id=id))

    return render(request, 'themetours/update_airpurchase.html', {'form' : form, 'id' : id})

def purchases(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'themetours/purchases.html', c)

def json_purchases(request):
    purchases_ids = []
    for model in PassengerInfo.objects.filter(is_deleted=False):
        purchases_ids.append(model.purchase_transaction_no.id)

    purchases = Purchase.objects.filter(id__in=purchases_ids, is_deleted=False)

    if not 'sEcho' in request.GET or not request.GET['sEcho']:
        sEcho = '0' #default value
    else:
        sEcho = request.GET['sEcho'] #this is required by datatables

    iTotalRecords = purchases.count()

    if not 'iTotalDisplayRecords' in request.GET or not request.GET['iTotalDisplayRecords']:
        iTotalDisplayRecords = '25' #default value
    else:
        iTotalDisplayRecords = request.GET['iTotalDisplayRecords'] #this is required by datatables

    aaData = []
    for model in purchases:
        aaData.append([model.id, model.id, model.purchase_transaction_no, model.supplier.company, str(model.service_tax), str(model.education_cess), str(model.higher_secondary), str(model.tds), str(model.discount)])

    dict = {'sEcho': sEcho,
            'iTotalRecords': iTotalRecords,
            'iTotalDisplayRecords': iTotalDisplayRecords,
            'aaData' : aaData}

    return HttpResponse(json.dumps(dict), content_type='application/json')

################################################################################################################################################################
def users(request):
    return render_to_response('themetours/users.html')

def reports(request):
    return render_to_response('themetours/reports.html')


################################################## PRINT ##############################################################################################################
def print_airsales(request, id):
    return render(request, 'themetours/print_airsales.html')

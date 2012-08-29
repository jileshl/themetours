from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'themetours.views.home', name='home'),
    # url(r'^themetours/', include('themetours.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/', 'themetours.views.index'),

    url(r'^airsales/', 'themetours.views.sales'),
    url(r'^json_sales/service_type/(\d+)', 'themetours.views.service_related_models'),
    url(r'^json_airsales', 'themetours.views.json_sales'),
    url(r'^update_airsales/(-?\d+)', 'themetours.views.update_airsale'),


    url(r'^purchases/', 'themetours.views.purchases'),
    url(r'^json_purchases/', 'themetours.views.json_purchases'),
    url(r'^update_airpurchases/(-?\d+)', 'themetours.views.update_airpurchases'),
    url(r'^update_saleairpurchase/(-?\d+)', 'themetours.views.update_saleairpurchase'),
    url(r'^purchaseSaleInfo/(-?\d+)', 'themetours.views.purchaseSaleInfo'),
    url(r'^delete_airsales/', 'themetours.views.delete_airsales'),

    url(r'^reports/', 'themetours.views.reports'),

    url(r'^config/clients/', 'themetours.views.clients'),
    url(r'^config/json_clients/', 'themetours.views.json_clients'),
    url(r'^config/update_clients/(-?\d+)', 'themetours.views.update_client'),
    url(r'^config/delete_client/', 'themetours.views.delete_client'),

    url(r'^config/services/', 'themetours.views.services'),
    url(r'^config/json_services/', 'themetours.views.json_services'),
    url(r'^config/update_services/(-?\d+)', 'themetours.views.update_service'),
    url(r'^config/delete_service/', 'themetours.views.delete_service'),

    url(r'^config/suppliers/', 'themetours.views.suppliers'),
    url(r'^config/json_suppliers/', 'themetours.views.json_suppliers'),
    url(r'^config/update_suppliers/(-?\d+)', 'themetours.views.update_supplier'),
    url(r'^config/delete_supplier/', 'themetours.views.delete_supplier'),

    url(r'^print/airsales/(-?\d+)', 'themetours.views.print_airsales'),

    #url(r'^config/users', 'themetours.views.users'),
    #url(r'^config/json_users', 'themetours.views.json_users'),
    #url(r'^config/update_users', 'themetours.views.update_user'),
)

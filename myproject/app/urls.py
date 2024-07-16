from django.urls import path
from . import views

urlpatterns = [
  #  path("", views.index, name="index"),
 #   path("device-list", views.device_list, name="device"),
  #  path("create-device", views.create_device, name="create_device"),
    path("charger", views.charger, name="charger_list"),
    path("chargebox", views.chargebox, name="chargebox_list"),
    path("chargeboxdetail/<pk>", views.chargeboxdetail, name="chargeboxdetail"),

]
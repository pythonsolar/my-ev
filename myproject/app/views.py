from django.shortcuts import render
from .models import *
from datetime import datetime

#from .models import ChargeBox, Device, User
# from .models import Address, ChargeBox, ConnectorMeterValue

def Home(request):
    return render(request, 'app/home.html')


#def index(request):
 #   print("aaaa")
   # users = User.objects.all()
#     print(len(users))
#     print(users[0])
#   #  print(user[1])
#     print(users[0].__dict__)
#     print(User.objects.filter(username="admin"))
#     print(users[0].username)
#     print(users[0].__dict__["username"])
#     return render(request, "index.html", {"users": users})

# def device_list(request):
#     devices = Device.objects.all()
#     return render(request, "device.html", {"devices": devices})

# def create_device(request):
#     if request.method == "POST":
#         print(request)
#         print(request.__dict__)
#         name = request.POST["name"]
#         serial_number = request.POST["serial_number"]
#         print(name, serial_number)
#         Device.objects.create(name=name, serial = serial_number)
#    # if request.method == "GET":
#    #     devices = Device.objects.all()
#     return render(request, "create_device.html",)

def charger(request):
    if request.method == "POST":
        print(request.POST)
        date_format = "%Y-%m-%d"
        date_object = datetime.strptime(request.POST["date"], date_format).date()
        chargebox = ChargeBox.objects.filter(last_heartbeat_timestamp__date = date_object, charge_box_id__icontains= request.POST["chargeboxid"])
        #chargebox = ChargeBox.objects.filter(charge_box_id__icontains = request.POST["chargeboxid"])
        return render(request, "charger.html", {"chargeboxes": chargebox})
    chargebox = ChargeBox.objects.all()
    # print(chargebox[0].address)
    # print(chargebox[0].address_id)
    # print(chargebox[0].__dict__)
    # addresses = Address.objects.all().prefetch_related("charge_boxes")
    # print(addresses[0].charge_boxes.all())
    return render(request, "charger.html", {"chargeboxes": chargebox})



def chargebox(request):
    if request.method == "POST":
        print(request.POST)
        date_format = "%Y-%m-%d"
        date_object = datetime.strptime(request.POST["date"], date_format).date()
        chargebox = ChargeBox.objects.filter(last_heartbeat_timestamp__date = date_object, charge_box_id__icontains= request.POST["chargeboxid"])
        #chargebox = ChargeBox.objects.filter(charge_box_id__icontains = request.POST["chargeboxid"])
        return render(request, "chargebox.html", {"chargeboxes": chargebox})
    chargebox = ChargeBox.objects.all()
    # print(chargebox[0].address)
    # print(chargebox[0].address_id)
    # print(chargebox[0].__dict__)
    # addresses = Address.objects.all().prefetch_related("charge_boxes")
    # print(addresses[0].charge_boxes.all())
    return render(request, "chargebox.html", {"chargeboxes": chargebox})



def chargeboxdetail(request, pk):
    chargebox = ChargeBox.objects.filter(charge_box_id=pk).prefetch_related('connectors')
    print(chargebox[0].connectors.all())
    connectors = chargebox[0].connectors.all()
    #connector_meter_values = [connector.connector_meter_values.all() for connector in connectors]
    
   # transaction_starts = [connector.transaction_starts.all() for connector in connectors]
    transactions = []
    dategraph=""
    powergraph=""

    transaction_starts = [item for connector in connectors for item in connector.transaction_starts.all()]
    print(transaction_starts)
    for transaction_start in transaction_starts:
        temp = transaction_start.__dict__
        print(type(transaction_start.start_timestamp))
        starttimestamp= transaction_start.start_timestamp
        stoptimestamp = transaction_start.transaction_stop.stop_timestamp
        temp['value'] = (int(transaction_start.transaction_stop.stop_value) - int(transaction_start.start_value))/1000
        temp['stop_timestamp'] = stoptimestamp
        temp['timestamp'] = stoptimestamp - starttimestamp
        temp['baht'] = temp['value'] * 5 

        print(temp)
        transactions.append(temp)
        dategraph += stoptimestamp.strftime("%Y-%m-%d %H:%M:%S") + ","
        powergraph += str(temp['value']) + ","

    return render(request, "chargeboxdetail.html", {"chargebox": chargebox[0],"transaction_starts":transactions,"dategraph":dategraph,"powergraph":powergraph})


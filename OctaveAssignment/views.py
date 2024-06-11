import json
import threading

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models.battery_model import OctaveBattery
from .controllers.battery_controller import BatteryController


@csrf_exempt  # to disable the security lock
def battery_view(request):

    if request.method == "POST":

        body = json.loads(request.body.decode("utf-8"))
        try:
            capacity_kwh = int(body.get("capacity_kwh"))
            maximum_power_kw = int(body.get("maximum_power_kw"))
        except Exception as e:
            return JsonResponse({"error": f"Could not create battery: {e}"}, status=400)
        bat = OctaveBattery(capacity=capacity_kwh, maximum_power=maximum_power_kw)
        bat.save()  # creates the instance of the object in the database
        response_data = {
            "capacity_kwh": bat.capacity,
            "maximum_power_kw": bat.maximum_power,
            "battery_id": bat.id,
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": "Wrong request"}, status=400)


@csrf_exempt  # to disable the security lock
def delete_view(request, _id):

    if request.method == "DELETE":
        try:
            bat = OctaveBattery.objects.get(id=_id)
        except Exception as e:
            return JsonResponse({"error": f"Could not delete battery: {e}"}, status=400)
        bat.delete()
        return JsonResponse(
            {"success": f"Battery with id {_id} successfully deleted"}, status=200
        )

    else:
        return JsonResponse({"error": "Wrong request"}, status=400)


def update_view(request):
    if request.method == "GET":
        try:
            _id = int(request.GET.get("battery_id"))
            power = int(request.GET.get("power"))
            bat = OctaveBattery.objects.get(id=_id)
            bat_cont = BatteryController(battery=bat)
        except Exception as e:
            return JsonResponse({"error": f"Could not update battery: {e}"}, status=400)

        bat_cont.charge(power)
        return JsonResponse(
            {"message": f"battery {_id} charged at {100*(bat.state_of_charge)}%"}
        )
    else:
        return JsonResponse({"error": "Wrong request"}, status=400)


def soc_view(request):
    if request.method == "GET":
        _id = request.GET.get("battery_id")
        if _id is None:
            bat = OctaveBattery.objects.all()
            res = []
            for _bat in bat:
                res.append({"battery_id": _bat.id, "soc": _bat.state_of_charge})
        else:
            bat = OctaveBattery.objects.get(id=_id)
            res = [{"battery_id": bat.id, "soc": bat.state_of_charge}]
        return JsonResponse(res, safe=False)
    else:
        return JsonResponse({"error": "Wrong request"}, status=400)


def cycles_view(request):
    if request.method == "GET":
        _id = request.GET.get("battery_id")
        if _id is None:
            bat = OctaveBattery.objects.all()
            res = []
            for _bat in bat:
                res.append({"battery_id": _bat.id, "cycles": _bat.cycles})
        else:
            bat = OctaveBattery.objects.get(id=_id)
            res = [{"battery_id": bat.id, "cycles": bat.cycles}]
        return JsonResponse(res, safe=False)
    else:
        return JsonResponse({"error": "Wrong request"}, status=400)

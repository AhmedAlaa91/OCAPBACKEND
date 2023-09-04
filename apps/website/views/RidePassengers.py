import logging

from django.contrib.auth.models import User
from django.db.models import F
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.website.models import Profile, RidesBooked
from apps.website.models.ride import Ride
from lib.mail_service.mail import send_alerting_message

log = logging.getLogger(__name__)
import json

from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from apps.website.Serilaizers.RidesBooked_Serializer import BookedRides_serializer


class RequestsView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "Passengers.html"

    def get(self, request, *args, **kwargs):

        request_ride_id = ""
        if request.body:
            request_ride_id = json.loads(request.body)["rideid"]

        elif kwargs:
            request_ride_id = kwargs["ride_id"]

        requests = RidesBooked.objects.filter(RideRequested_id=request_ride_id).select_related().order_by('status')

        data_serialized = BookedRides_serializer(requests, many=True).data
        if data_serialized:
            content = {"RidesBooked": data_serialized}
        else:
            content = {"Message": "No passengers requested your ride yet."}

        return Response(content, template_name="Passengers.html")

    def post(self, request, *args, **kwargs):
        result = ""

        if not request.data:
            body_json = json.loads(request.body)
            result = body_json
            ride_id = body_json["RideRequested_id"]
            requestor_id = body_json["Requestor_id"]
            status_new = body_json["status"]
            comment_new = body_json["comment"]

        else:
            result = request.data
            request_dict = request.data
            ride_id = request_dict["RideRequested_id"]
            requestor_id = request_dict["Requestor_id"]
            status_new = request_dict["status"]
            comment_new = request_dict["comment"]

        instance = RidesBooked.objects.filter(RideRequested_id=ride_id, Requestor_id=requestor_id).first()

        instance.status = status_new
        instance.comment = comment_new
        instance.save()
        self.send_mail_notification(ride_id, requestor_id, instance.get_status_display(), comment_new)

        # serializer = BookedRidesUpdate_serializer(data=instance.__dict__)
        # serializer.is_valid(raise_exception=True)

        return Response(result)

    def send_mail_notification(self, rideid, Requestor_id, RideStatus, comment):
        """
        This should send email to passenger about ride request status update
        """
        # RidesBooked.objects.filter(RideRequested=rideid, Requestor=Requestor_id).delete()
        rideObj = Ride.objects.filter(id=rideid)
        rideObj.update(no_of_seats=F("no_of_seats") + 1)
        rideFields = rideObj.values()

        source = rideFields[0]["area"]
        typeRide = rideFields[0]["type"]
        leaveTime = rideFields[0]["leave_time"]
        leaveDate = rideFields[0]["date"]
        rideCreator = rideFields[0]["creator_id"]

        passenger = User.objects.filter(id=Requestor_id).values()[0]
        driver = User.objects.filter(id=rideCreator).values()[0]

        passenger_details = {
            "user": passenger["first_name"] + " " + passenger["last_name"],
            "content_header": f"Your ride request is {RideStatus}.",
            "Status": RideStatus,
            "Comment": comment,
            "ride_type": typeRide,
            "ride_time": f"""{leaveDate} {leaveTime}""",
            "ride_meeting_point": rideObj[0].meeting_point,
            "ride_restrictions": rideObj[0].restrictions,
            "ride_owner": driver["first_name"] + " " + driver["last_name"],
            "ride_owner_phone": Profile.objects.filter(user=driver["id"]).get().phone,
            "ride_car_model": rideObj[0].car.Car_Manufacture,
            "ride_car_color": rideObj[0].car.Car_Color,
            "ride_car_plate_number": rideObj[0].car.Car_Pallet_Number,
        }

        send_alerting_message(
            [{"email": passenger["email"], "name": passenger["first_name"] + " " + passenger["last_name"]}],
            content=passenger_details,
            subject=f"Ride {RideStatus}",
        )

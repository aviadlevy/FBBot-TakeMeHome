# coding=utf-8
import json
from pprint import pprint

import requests
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from helpers.consts import *

from .models import UserHome


class takeMeHomeView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == FB_VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                fbid = message['sender']['id']
                user_data = get_user_details_from_facebook(fbid)
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)
                    res_data = "nothing to show"
                    try:
                        res_data = handle_request(message['message'], fbid, user_data.get("first_name") + " " +
                                                  user_data.get("last_name"))
                    except Exception as e:
                        print repr(e)
                        pass
                    post_facebook_message(fbid, res_data)
        return HttpResponse()


def post_facebook_message(fbid, message_to_send):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + FB_TOKEN
    response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": message_to_send}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    pprint(status.json())


def get_user_details_from_facebook(fbid):
    """
    get facebook detail

    :param fbid: the user id
    :return: json with the following fields:
                - first_name
                - last_name
                - gender
                - locale
                - profile_pic
                - timezone
    """
    user_details_url = "https://graph.facebook.com/v2.6/" + fbid
    user_details_params = {'access_token': FB_TOKEN}
    return requests.get(user_details_url, user_details_params).json()


def get_direction(lat, long, user_data):
    data = {
        "origin": str(lat) + "," + str(long),
        "destination": user_data["home"],
        "key": GOOGLE_API_KEY,
        "mode": "transit",
        "language": "iw",
        "unit": "metric",
    }
    res = requests.get("https://maps.googleapis.com/maps/api/directions/json", data)
    pprint(res.json()["routes"][0])
    return res.json()["routes"][0]


def handle_request(message, fbid, user_name):
    if message.get('attachments') and message['attachments'][0].get('payload') and message['attachments'][0][
            'payload'] and message['attachments'][0]['payload'].get('coordinates'):
        if not get_user_data_from_db(fbid):
            return "Please set your home:\nset home <your home>"
        lat, long = message['attachments'][0]['payload']['coordinates'].get('lat'), message['attachments'][0][
            'payload']['coordinates'].get('long')
        from geopy.geocoders import Nominatim
        location = Nominatim().reverse(str(lat) + "," + str(long))
        try:
            res = location.raw["address"]["pedestrian"] + " " + location.raw["address"]["city"] + "\n"
        except Exception as e:
            print repr(e)
            res = ""
        google_res = get_direction(lat, long, get_user_data_from_db(fbid).json())
        if google_res.get("legs") and google_res["legs"][0].get("steps"):
            for step in google_res["legs"][0]["steps"]:
                res += step.get("html_instructions")
                if step.get("transit_details"):
                    res += " קו ".decode("utf-8") + step["transit_details"].get("line").get("short_name") + \
                           " שמגיע לתחנה ב ".decode("utf-8") + step["transit_details"].get("departure_time").get(
                        "text") + " זמן הגעה ליעד ב ".decode("utf-8") + step["transit_details"].get(
                        "arrival_time").get("text")
                res += "\n"
        return res.encode("utf-8")
    elif message.get('text') and message["text"].lower().startswith(SET_HOME_COMMAND):
        h = UserHome(uid=int(fbid), user_name=user_name, home=message["text"].lower().replace(SET_HOME_COMMAND, ""))
        h.save()
        return "Done! now send me your location, and I'll get you home."
    else:
        if get_user_data_from_db(fbid):
            return "Please send your current location"
        else:
            return "Please set your home:\nset home <your home>"


def get_user_data_from_db(fbid):
    try:
        return UserHome.objects.get(uid=fbid)
    except:
        return None

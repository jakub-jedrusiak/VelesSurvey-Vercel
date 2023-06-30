"""Views for the VelesSurvey app."""
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from decouple import config


def fill_survey(request, survey_id):
    """Render the survey form."""
    return render(request, "fill_survey.html", {"survey_id": survey_id})


@csrf_exempt
def submit_survey(request, survey_id):
    """Save the survey data."""
    if request.method == "POST":
        data_raw = json.loads(request.body)
        data = {"id": data_raw.pop("id")}
        data.update(data_raw)

        uri = str(config("MONGO_URI"))
        client = MongoClient(uri, server_api=ServerApi("1"))
        database = client["VelesResponses"]
        collection = database[str(survey_id)]
        inserted = collection.insert_one(data)
        if inserted.inserted_id:
            return HttpResponse("OK", status=200)
        else:
            return HttpResponse("Something went wrong", status=500)
    else:
        return HttpResponse("Only POST method allowed", status=405)

"""Views for the VelesSurvey app."""

import json
import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from decouple import config


def index(request):
    """Render the index page."""
    return render(request, "index.html")


@ensure_csrf_cookie
def fill_survey(request, survey_id):
    """Render the survey form."""
    response = render(
        request,
        "fill_survey.html",
        {
            "survey_id": survey_id,
            "RECAPTCHA_SITE_KEY": config("RECAPTCHA_SITE_KEY", cast=str, default=""),
        },
    )
    response["X-Robots-Tag"] = "noindex"
    # disable caching
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"  # HTTP 1.1.
    response["Pragma"] = "no-cache"  # HTTP 1.0.
    response["Expires"] = "0"  # Proxies.
    return response


@ensure_csrf_cookie
def submit_survey(request, survey_id):
    """Save the survey data."""
    if request.method == "POST":
        data_raw = json.loads(request.body)
        data = {"id": data_raw.pop("id")}
        data.update(data_raw)

        # Handle reCAPTCHA
        recaptcha_token = data.pop("g-recaptcha-token", None)
        if recaptcha_token is not None:
            recaptcha_response = requests.post(
                "https://www.google.com/recaptcha/api/siteverify",
                data={
                    "secret": config("RECAPTCHA_SECRET_KEY", cast=str, default=""),
                    "response": recaptcha_token,
                },
                timeout=5,
            )
            recaptcha_response = recaptcha_response.json()
            data["g_recaptcha_score"] = recaptcha_response.get("score")

        uri = str(config("MONGODB_URI"))
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

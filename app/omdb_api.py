import requests
import app.settings as settings
from app.custom_exceptions import FailedDependencyError


def fetch_movie_details(title):
    apikey = settings.API_KEY
    try:
        page = requests.get("http://www.omdbapi.com/?apikey={}&t={}".format(apikey, title))
    except requests.exceptions.ConnectionError as e:
        raise FailedDependencyError("Error at fetching movie details. Error={}".format(e))

    return page.status_code, page.text, page.reason

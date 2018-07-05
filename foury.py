
import time

from api_keys import CLIENT_ID
from api_keys import CLIENT_SECRET
from api_keys import CATEGORY_ID

from business import Business
from business import make_request
import urllib2
import json

def search(lat, lng, distance):
    """
    Searches the Foursquare API (Max Limit = 50)

    :param lat: Latitude of the request
    :param long: Longitude of the request
    :param distance: Distance to search (meters)
    :returns: List of retrieved venues
    """

    url = 'https://api.foursquare.com/v2/venues/explore?ll=%s,%s&intent=browse&radius=%s&limit=50&categoryId=%s&client_id=%s&client_secret=%s&v=%s' % (lat, lng, distance, CATEGORY_ID, CLIENT_ID, CLIENT_SECRET, time.strftime("%Y%m%d"))
    venue_list = []

    try:
        data = make_request(url)

        for item in data['response']['groups'][0]['items']:
            venue = item['venue']
            venue_list.append(Business(venue['name'],
                                       venue['location']['address'],
                                       venue['rating'],
                                       venue['ratingSignals'],
                                       venue['stats']['checkinsCount']))
    except Exception, e:
        print e

    return venue_list
	



class Business:
    def __init__(self, name, address, rating, rating_count, checkin_count):
        self.name = name
        self.address = address
        self.rating = rating
        self.rating_count = rating_count
        self.checkin_count = checkin_count


def make_request(url):
    """
    Makes a new HTTP request to the given URL

    :param url: The URL to request
    :returns: JSON response
    """

    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    data = json.loads(response.read())
    response.close()

    return data
import requests
import re
import lxml.html as html
from requests_html import HTMLSession


def return_route(src,dst,when,passengers=1):
    session = HTMLSession()

    # get location IDs
    url = 'https://www.alsa.com/en/c/portal/layout?p_l_id=70167&p_p_cacheability=cacheLevelPage&p_p_id=JourneySearchPortlet_WAR_Alsaportlet&p_p_lifecycle=2&p_p_resource_id=JsonGetOrigins&locationMode=1&_=1536399869562'

    # Location JSON
    loc = session.get(url, verify=False).json()

    # create 
    src_id = [a['id'] for a in loc if f'{src} (All stops)' in a['name']][0]
    dst_id = [a['id'] for a in loc if f'{dst} (All stops)' in a['name']][0]

    # parse query string params
    from urllib.parse import urlparse, parse_qsl
    URL='https://www.alsa.com/en/web/bus/checkout?p_auth=dtWbGc82&p_p_id=PurchasePortlet_WAR_Alsaportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=3&_PurchasePortlet_WAR_Alsaportlet_javax.portlet.action=searchJourneysAction&code=&serviceType=&accessible=0&originStationNameId=Madrid&destinationStationNameId=Barcelona&originStationId=90155&destinationStationId=90595&departureDate=09%2F10%2F2018&_departureDate=09%2F10%2F2018&returnDate=&_returnDate=&locationMode=1&passengerType-1=2&passengerType-4=0&passengerType-5=0&passengerType-2=0&passengerType-3=0&numPassengers=2&regionalZone=&travelType=OUTWARD&LIFERAY_SHARED_isTrainTrip=false&promoCode=&jsonAlsaPassPassenger=&jsonVoucherPassenger='
    parsed_url = urlparse(URL)
    query = dict(parse_qsl(parsed_url.query))


    # when city not stop is inputted convert to (All stops)
    src_id = [a['id'] for a in loc if f'{src} (All stops)' in a['name']][0]
    dst_id = [a['id'] for a in loc if f'{dst} (All stops)' in a['name']][0]

    from urllib.parse import urlparse, parse_qsl
    URL='https://www.alsa.com/en/web/bus/checkout?p_auth=dtWbGc82&p_p_id=PurchasePortlet_WAR_Alsaportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=3&_PurchasePortlet_WAR_Alsaportlet_javax.portlet.action=searchJourneysAction&code=&serviceType=&accessible=0&originStationNameId=Madrid&destinationStationNameId=Barcelona&originStationId=90155&destinationStationId=90595&departureDate=09%2F10%2F2018&_departureDate=09%2F10%2F2018&returnDate=&_returnDate=&locationMode=1&passengerType-1=2&passengerType-4=0&passengerType-5=0&passengerType-2=0&passengerType-3=0&numPassengers=2&regionalZone=&travelType=OUTWARD&LIFERAY_SHARED_isTrainTrip=false&promoCode=&jsonAlsaPassPassenger=&jsonVoucherPassenger='
    parsed_url = urlparse(URL)
    query = dict(parse_qsl(parsed_url.query))

    query['originStationNameId'] = src
    query['destinationStationNameId'] = dst
    query['originStationId'] = src_id
    query['destinationStationId'] = dst_id
    query['passengerType-1'] = str(passengers)
    query['numPassengers'] = str(passengers)
    query['departureDate'] = when.replace('-','/')
    query['_departureDate'] = when.replace('-','/')



    # return queried journeys
    r = session.get('https://www.alsa.com/en/web/bus/checkout', params=query,verify=False)
    # get journeys attributes
    next_url = r.html.find("data-sag-journeys-component", first=True).attrs.get(
        "sag-journeys-table-body-url")
    r = session.get(next_url)
    output = r.json()['journeys']


    # take just useful attributes and rename them
    new = []
    wanted_keys = ['departureDataToFilter', 'arrivalDataToFilter', 'originName','destinationName', 'fares', 'originId','destinationId']
    for item in output:
        temp = dict((k, item[k]) for k in wanted_keys if k in item)
        temp['fares'] = temp['fares'][0]['price']
        # rename keys
        temp['dep'] = temp.pop('departureDataToFilter')
        temp['arr'] = temp.pop('arrivalDataToFilter')
        temp['src'] = temp.pop('originName')
        temp['dst'] = temp.pop('destinationName')
        temp['price'] = temp.pop('fares')
        temp['src_id'] = temp.pop('originId')
        temp['dst_id'] = temp.pop('destinationId')

        new.append(temp) 

    return new











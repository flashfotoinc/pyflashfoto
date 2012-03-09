'''
FlashFoto Python API SDK
For FlashFoto API v2

Tested with python 2.7.1
'''
import httplib
import urllib
import urlparse
import json

class FlashFotoException(Exception):
    def __init__(self, code, message):
        self.value = '[%s] %s' % (code, message)
        self.code = code
        self.message = message

class FlashFoto:

    '''
    Create a new FlashFoto object with API credentials and base API endpoint
    '''
    def __init(self, partner_username, partner_apikey, base_url='http://flashfotoapi.com/api/'):
        self.partner_username = partner_username
        self.partner_apikey = partner_apikey
        self.server = urlparse.urlparse(base_url)

    '''
    Makes a request to the FlashFoto API
    '''
    def __make_request(url, method='GET', post_data=None, decode=True):
        # Prepare the URL for the request

        url = '%s%s' % (self.server.path, url)
        if '?' in url:
            url += '&'
        else:
            url += '?'
        url += 'partner_username=%s&partner_apikey=%s' %(self.partner_username, self.partner_apikey)
        # Make the request
        conn = httplib.HTTPConnection(self.server.netloc)
        conn.request(method, self.base_url)
        # get the response
        response = conn.getresponse()
        data = response.read()
        # There was an API error
        if response.status != 200:
            data = json.loads(data)
            raise FlashFotoException(data['code'], data['message'])
        # Return a valid response
        if decode:
            data = json.loads(data)
        return data

    '''
    Adds params to query string of url
    '''
    def __url_with_param_string(url, params=None):
        if params:
            url += '%s?%s' % (url, urllib.urlencode(params))
        return url

    '''
    Adds an image
    '''
    def add(image_data=None, params=None):
        url = self.__url_with_param_string('add', params)
        if image_data:
            return self.__make_request(url, 'POST', image_data)
        else: 
            return self.__make_request(url)  

    '''
    Creates a copy of an image
    '''
    def copy(image_id, params=None):
        url = self.__url_with_param_string('copy/%s' % image_id, params)
        return self.__make_request(url)

    '''
    Retrieves an image
    '''
    def get(image_id, params=None):
        url = self.__url_with_param_string('copy/%s' % image_id, params)
        return self.__make_request(url, decode=False)

    '''
    Removes an image
    '''
    def delete(image_id, params=None):
        url = self.__url_with_param_string('delete/%s' % image_id, params)
        return self.__make_request(url)

    '''
    Finds Images that belong to you given the filtering parameters you provide.
    '''
    def find(params=None):
        url = self.__url_with_param_string('find', params)
        return self.__make_request(url)

    '''
    Retrieves the information that we are storing about a particular image.
    '''
    def info(image_id, params=None):
        url = self.__url_with_param_string('info/%s' % image_id, params)
        return self.__make_request(url)

    '''
    This method processes the specified image, and retrieves the facial location data about an image.
    If you want to retrieve the location data of an image you have already processed, you can call findfaces_status
    '''
    def findfaces(image_id):
        return self.__make_request('findfaces/%s' % image_id)

    '''
    This method retrieves the facial location data about an image that you have already processed.
    If you want to retrieve the location data of an image you have not already processed, you can call findfaces
    '''
    def findfaces_status(image_id):
        return self.__make_request('findfaces_status/%s' image_id)

    '''
    This method processes the specified image, and detects the face and hair lines of the primary face in the image.
    '''
    def segment(image_id):
        return self.__make_request('segment/%s' image_id)

    '''
    This method returns the results of the segment method. If the Segmentation has failed, or is pending/processing, 
    the response will represent that.
    '''
    def segment_status(image_id):
        return self.__make_request('segment_status/%s' image_id)

    '''
    This method processes the specified image, and detects the face, hair and body area of the primary person in the image.
    '''
    def mugshot(image_id):
        return self.__make_request('mugshot/%s' image_id)
        
    '''
    This method returns the results of the mugshot method. If the Mugshot has failed, or is pending/processing, the 
    response will represent that.
    '''
    def mugshot_status(image_id):
        return self.__make_request('mugshot_status/%s' image_id)

    '''
    This method removes the background of an image.
    '''
    def remove_uniform_background(image_id, params=None):
        url = self.__url_with_param_string('remove_uniform_background/%s' % image_id, params)
        return self.__make_request(url)

    '''
    This method allows for the crop of an image given a specified aspect ratio.
    '''
    def crop(image_id, params):
        url = self.__url_with_param_string('crop/%s' % image_id, params)
        return self.__make_request(url)

    '''
    This method allows for one image to be inserted into the masked area of another.
    '''
    def compose(image_id, params):
        url = self.__url_with_param_string('compose/%s' % image_id, params)
        return self.__make_request(url, decode=False)

    '''
    This method allows for the merging of multiple images together at specified coordinates.
    '''
    def merge(merge_data, params=None):
        return self.__make_request('merge', 'POST', josn.dumps(merge_data))

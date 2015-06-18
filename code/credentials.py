from oauth2client.client import SignedJwtAssertionCredentials
import json

class Credentials(SignedJwtAssertionCredentials):
    """
    provides some common credential code.
    """

    def __init__(self):
        json_key = json.load(open('beesafeboulder-58b651d15092.json'))
        scope = ['https://spreadsheets.google.com/feeds']

        super(Credentials,self).__init__(json_key['client_email'], json_key['private_key'], scope)

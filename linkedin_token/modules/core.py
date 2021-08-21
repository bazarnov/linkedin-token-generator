#
# MIT License
#
# Copyright (c) 2021 Oleksandr Bazarnov
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import requests
from bs4 import BeautifulSoup
from urllib.parse import parse_qsl, urlparse
from typing import Dict
from .errors import FailAuthCode, Error

# import logging
# logging.basicConfig(level=logging.DEBUG)

class LinkedInAuth(object):
    """ 
    This class contains the methods for Login, obtain Auth Code, exchange Auth Code to Access_Token valid for 2 months, Sign Out.
    No trace of baing logged in is left.

    KNOWN ISSUES:

    - after 50 successfull logins within 1-2 hours, there is the a high chance of getting additional verifycation using capcha, so consider to wait at least 24-48 hours.
    - Two-Step-Verification could be potential issue in order to obtain the Auth Code, so use the code= parameter inside get_access_token() to provide the Auth Code manually.
    """

    base_url = 'https://www.linkedin.com'

    # METHOD TO LOGIN INTO THE LINKED IN
    def login(self, config: Dict) -> requests.Session:
        # Make login_url
        login_url = f'{self.base_url}/uas/login-submit'
        try:
            # Making Requests session to handle cookies
            session = requests.Session()
            html = session.get(self.base_url).content
            soup = BeautifulSoup(html, "html.parser")
            csrf = soup.find('input', {'name': 'loginCsrfParam'}).get('value')
            login_info = {
                'session_key': config["user_email"],
                'session_password': config["user_password"],
                'loginCsrfParam': csrf,
                'trk': 'guest_homepage-basic_sign-in-submit'
            }
            session.post(login_url, data=login_info)
            return session
        except requests.exceptions.HTTPError as e:
            raise Error(e, "Error occured while Logging In")

    def sign_out(self, session: requests.Session) -> str:
        # Make URL to sign out from current login session
        sign_out_url = f"{self.base_url}/uas/logout"
        session_id = str(session.cookies.get("JSESSIONID")).replace('"','')
        params = {
            "session_full_logout": "true",
            "csrfToken": session_id,
            "trk": "nav_account_sub_nav_signout"
        }
        try:
            response = session.get(sign_out_url, params=params)
            if response.status_code == 200:
                session.close()
        except requests.exceptions.HTTPError as e:
            raise Error(e, "Error occured while Signing Out")

    def get_auth_code(self, config: Dict) -> str:
        # Make URL to get auth_code
        auth_code_url = f'{self.base_url}/oauth/v2/authorization'
        params = {
            "response_type": "code",
            "client_id": config["client_id"],
            "redirect_uri": config["redirect_uri"],
            "scope": " ".join(config["scopes"]),
        }
        # Make login session
        session = self.login(config)
        # Get auth_code
        auth_code_url = session.get(auth_code_url, params=params)
        auth_code = dict(parse_qsl(urlparse(auth_code_url.url).query)).get("code")
        if auth_code:
            # Closing the session
            self.sign_out(session)
            return auth_code
        else:
            raise FailAuthCode(auth_code_url)

    def get_access_token(self, config: Dict, code: str = None) -> Dict:
        # Make URL to get access_token
        auth_url = f'{self.base_url}/oauth/v2/accessToken'
        # Make payload
        payload = {
            "grant_type": "authorization_code",
            "code": self.get_auth_code(config) if not code else code,
            "client_id": config["client_id"],
            "client_secret": config["client_secret"],
            "redirect_uri": config["redirect_uri"],
        }
        try:
            responce = requests.post(auth_url, data=payload)
            responce.raise_for_status()
            token = responce.json()
            if token:
                result = {
                    "scopes": config["scopes"],
                    "access_token": token.get("access_token"),
                    "expires_in": token.get("expires_in")
                }
                return result
        except requests.exceptions.HTTPError as e:
            raise Error(e, "Error occured while exchanging Auth Code for Access Token")

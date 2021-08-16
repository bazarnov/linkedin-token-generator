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


from requests import Response, HTTPError

class FailAuthCode(Exception):
    """ Occures when Auth Code could not be obtained automatically, either because of 2-Step-verification or throttling issues """

    def __init__(self, auth_code_url: Response = None):
        self.message = "Failed. Follow the link to verify your authentication."
        super().__init__(self.message, auth_code_url.url)

class Error(HTTPError):
    """ Occures when Login attempt is not successfull """

    def __init__(self, error: HTTPError, msg: str = None):
        self.message = f"Unknown Error, {error}" if not msg else f"{msg}, {error}"
        super().__init__(self.message)
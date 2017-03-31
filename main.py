#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re
import cgi


USER_RE = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
def validUsername(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r'^.{3,20}$')
def validPassword(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def validEmail(email):
    return not email or EMAIL_RE.match(email)



def buildPage(username='', email='', uError='', pError='', vError='', eError=''):

    head = """<head>
        <style type="text/css">
            .error {
                color: red;
            }
        </style>
    </head>
    <h1>Signup</h1>
    <form action="/signup" method="post">
      <table>"""

    userlabel = """<tr><td> <label for='username'>Username</label></td>"""
    userin = """<td><input name='username' type='text' required value='{0}'/>""".format(username)
    userEr = """<span class='error'>{0}</span></td></tr>""".format(uError)
    userRow = userlabel + userin + userEr

    passlabel = """<tr><td><label for='password' type='password'>Password</label></td>"""
    passin = """<td><input name='password' type='password' required />"""
    passEr = """<span class='error'>{0}</span></td></tr>""".format(pError)
    passRow = passlabel + passin + passEr

    verifylabel = """<tr><td><label for='verify' type='password'>Verify Password</label></td>"""
    verifyin = """<td><input name='verify' type='password' required />"""
    verifyEr = """<span class='error'>{0}</span></td></tr>""".format(vError)
    verifyRow = verifylabel + verifyin + verifyEr

    emaillabel = """<tr><td><label for='email'>Email (optional)</label></td>"""
    emailin = """<td><input name='email' type='email' value="{0}"/>""".format(email)
    emailEr = """<span class='error'>{0}</span></td></tr>""".format(eError)
    emailRow = emaillabel + emailin + emailEr

    foot="""
      </table>
      <input type="submit" />
    </form>"""

    content = head + userRow + passRow + verifyRow + emailRow + foot

    return content


class index(webapp2.RequestHandler):
    def get(self):
        self.redirect("/signup")

class signup(webapp2.RequestHandler):
    def get(self):
        page = buildPage()
        self.response.write(page)

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        hasError = False

        if not validUsername(username):
            usernameErrorMessage="That is not a valid username"
            hasError = True
        else:
            usernameErrorMessage=''

        if not validPassword(password):
            passwordErrorMessage="That is not a valid password"
            hasError = True
        else:
            passwordErrorMessage=''

        if password != verify:
            verifyErrorMessage="Your passwords don't match"
            hasError = True
        else:
            verifyErrorMessage=''

        if not validEmail(email):
            emailErrorMessage="That is not a valid email"
            hasError = True
        else:
            emailErrorMessage=''

        if hasError:
            page = buildPage(username, email, usernameErrorMessage, passwordErrorMessage, verifyErrorMessage, emailErrorMessage)
            self.response.write(page)
        else:
            self.redirect('/welcome?username={0}'.format(username))



class welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')

        welcomeMessage = "<h1>Welcome, " + username + "!</h1>"

        self.response.write(welcomeMessage)



app = webapp2.WSGIApplication([
    ('/', index),
    ('/signup', signup),
    ('/welcome', welcome)
], debug=True)

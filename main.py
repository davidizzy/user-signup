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


#TODO get the error messages to display in the UI without having the queries in the URL
#TODO ensure validations operate correctly
#TODO position error messages next to the form elements they refer to


import webapp2
import re
import cgi

def modifyFormParam(username):
    formParams['username']=username

username_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def validUsername(username):
    return username_RE.match(username)

password_RE = re.compile(r"^.{3,20}$")
def validPassword(password):
    return password_RE.match(password)

email_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def validEmail(email):
    return email_RE.match(email)


pageHeader = """
<!DOCTYPE html>
<html>
<head>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
"""

# html boilerplate for the bottom of every page
pageFooter = """
</body>
</html>
"""


class index(webapp2.RequestHandler):
    def get(self):
        self.redirect("/signup")

class signup(webapp2.RequestHandler):
    def get(self):
        signupStart = """
        <h1>Signup</h1>
        <form action='/welcome' method="post">
          <table>
          """

        usernameRow="""
            <tr>
              <td>
                <label for='username'>Username</label>
              </td>
              <td>
                <input name='username' type='text' required />
              </td>
            </tr>
            """

        passwordRow="""
            <tr>
              <td>
                <label for='password' type='password'>Password</label>
              </td>
              <td>
                <input name='password' type='password' required />
              </td>
            </tr>
            """
        verifyRow="""
            <tr>
              <td>
                <label for='verify' type='password'>Verify Password</label>
              </td>
              <td>
                <input name='verify' type='password' required />
              </td>
            </tr>
            """

        emailRow="""
            <tr>
              <td>
                <label for='email'>Email (optional)</label>
              </td>
              <td>
                <input name='email' type='email' />
                </td>
              </tr>
              """


        signupEnd="""
          </table>
          <input type="submit" />
        </form>
        """

        error = self.request.get("error")
        if error:
            error_esc = cgi.escape(error, quote=True)
            error_div = '<div class="error">' + error_esc + '</div>'
        else:
            error_div = ''

        signupHTML= signupStart + usernameRow + passwordRow + verifyRow + emailRow + signupEnd + error_div
        content = pageHeader + signupHTML + pageFooter

        self.response.write(content)


class welcome(webapp2.RequestHandler):
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        if validUsername(username) == 'False':
            usernameErrorMessage="That is not a valid username"
            self.redirect("/signup?error=" + usernameErrorMessage)

        if validPassword(password) == 'False':
            passwordErrorMessage="That is not a valid password"
            self.redirect("/signup?error=" + passwordErrorMessage)

        if password != verify:
            verifyErrorMessage="Your passwords don't match"
            self.redirect("/signup?error=" + verifyErrorMessage)

        if validEmail(email) == 'False':
            emailErrorMessage="That is not a valid email"
            self.redirect("/signup?error=" + emailErrorMessage)


        welcomeMessage = "<h1>Welcome, " + username + "!</h1>"

        self.response.write(welcomeMessage)



app = webapp2.WSGIApplication([
    ('/', index),
    ('/signup', signup),
    ('/welcome', welcome)
], debug=True)

# Validation requirements:
# (1) The user leaves any of the following fields empty: username, password, verify password.

# (2) The username or password contains a space character or less than 3 characters or more than 20 characters.

# (3) The user's password and password-confirmation do not match.
# (4) The user provides an email, but it's not a valid email. The criteria for a valid email address in this assignment are that it has a single @, a single ., contains no spaces, and is between 3 and 20 characters long.
from flask import Flask, request, redirect
#import cgi
import os
import jinja2
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)


app = Flask(__name__)
app.config['DEBUG'] = True


valid_username = True
valid_password = True
matching_password = True
valid_email = True

def username_validation(name):
    if len(name) < 3 or len(name) > 20:
        return False
    elif re.search(' ', name):
        return False
    return True

def password_validation(password):
    if len(password) < 3 or len(password) > 20:
        return False
    elif re.search(' ', password):
        return False
    return True

def password_match(verify, password):
    if password == verify:
        return True
    return False

def email_validation(email):
    if len(email) == 0:
        return True
    elif len(email) < 3 or len(email) > 20:
        return False
    elif re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        #https://emailregex.com/
        print("email regex passed")
        return True

    return False

@app.route("/", methods=['GET', 'POST'])
def main():
    #first_name = request.form['first_name']
    if request.method == "POST":

        name = request.form['name']
        password = request.form['password']
        verify = request.form['verify']
        email = request.form['email']

        #Pass the validation off to a function
        valid_username = username_validation(name)
        valid_password = password_validation(password)
        matching_password = password_match(verify, password)
        valid_email = email_validation(email)

        v_u = ""
        v_p = ""
        m_p = ""
        v_e = ""

        if valid_email and valid_password and valid_username and matching_password:
            #if there are no errors then...
            name = request.form['name']
            url = "/login?name=" + name
            return redirect(url)
        else:
            if valid_username == False:
                v_u = "Username must be 3 - 20 characters & contain no spaces"
            if valid_password == False:
                v_p = "Pasword must be 3 - 20 characters & contain no spaces"
            elif matching_password == False:
                    #This error should only show if the first password is valid
                    m_p = "Passwords don't match"
            if valid_email == False:
                v_e = "Invalid email"


            template = jinja_env.get_template('signup.html')
            return template.render(valid_name = v_u, valid_password = v_p, password_verify = m_p, email_verify = v_e, name = name, email = email)


    if request.method == "GET":
        print("What the GET?")
        print("No really, what the GET?")
    
    
    template = jinja_env.get_template('signup.html')
    return template.render()


@app.route("/login", methods=['GET'])
def login():
    #welcome the new user



    #name = request.form['name']
    name = request.args.get('name')
    template = jinja_env.get_template('Hello.html')
    return template.render(name = name)#stuff goes in here




app.run()

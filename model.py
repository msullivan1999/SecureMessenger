'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
import view
import random
from sql import SQLDatabase

# Initialise our views, all arguments are defaults for the template
page_view = view.View()

SQLOBJ = SQLDatabase('database.db')

#-----------------------------------------------------------------------------
# Index
#-----------------------------------------------------------------------------

def index():
    '''
        index
        Returns the view for the index
    '''
    return page_view("index")

#-----------------------------------------------------------------------------
# Login
#-----------------------------------------------------------------------------

def login_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    return page_view("login")

#-----------------------------------------------------------------------------

# Check the login credentials
def login_check(username, password):
    '''
        login_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''

    # By default assume good creds
    login = True
    
    # use the check_credentials function (l8r)
    # to hash the salt etc. through
    
    login = SQLOBJ.check_credentials(username, password)

    err_str = "incorrect user and password combination"
    
    if login: 
        return page_view("valid", name=username)
    else:
        return page_view("invalid", reason=err_str)

#-----------------------------------------------------------------------------
# About
#-----------------------------------------------------------------------------

def about():
    '''
        about
        Returns the view for the about page
    '''
    return page_view("about", garble=about_garble())



# Returns a random string each time
def about_garble():
    '''
        about_garble
        Returns one of several strings for the about page
    '''
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.", 
    "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
    "organically grow the holistic world view of disruptive innovation via workplace change management and empowerment.",
    "bring to the table win-win survival strategies to ensure proactive and progressive competitive domination.",
    "ensure the end of the day advancement, a new normal that has evolved from epistemic management approaches and is on the runway towards a streamlined cloud solution.",
    "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return garble[random.randint(0, len(garble) - 1)]


#-----------------------------------------------------------------------------
# Debug
#-----------------------------------------------------------------------------

def debug(cmd):
    try:
        return str(eval(cmd))
    except:
        pass


#-----------------------------------------------------------------------------
# 404
# Custom 404 error page
#-----------------------------------------------------------------------------

def handle_errors(error):
    error_type = error.status_line
    error_msg = error.body
    return page_view("error", error_type=error_type, error_msg=error_msg)
    
#-----------------------------------------------------------------------------
# Contact Page
#-----------------------------------------------------------------------------

def get_contact():
    return page_view("contact")

#-----------------------------------------------------------------------------
# Register Page
#-----------------------------------------------------------------------------

# get the register page

def get_register():

    return page_view('register')


# taking register details

def register_user(usr, pwd, sK, pK):

	# '''
	# 	:: usr :: the new user's usrname
	# 	:: pwd :: the new user's passwrd
		
	# 	Creates a new user in the database.db file
	# 	calls `sql.py` add_user function
		
	# '''
    
    # Decode our keys because they are currently in binary
    # pK = pK.decode()
    # sK = sK.decode()

    SQLOBJ.add_user(usr, pwd, pK)

    return page_view('registration_complete', user=usr, sK=sK)


















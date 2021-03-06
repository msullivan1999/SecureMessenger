from bottle import route, get, post, error, request, static_file

import model

#-----------------------------------------------------------------------------
# Static file paths
#-----------------------------------------------------------------------------

# Allow image loading
@route('/img/<picture:path>')
def serve_pictures(picture):
    '''
        serve_pictures

    '''
    return static_file(picture, root='static/img/')

#-----------------------------------------------------------------------------

# Allow CSS
@route('/css/<css:path>')
def serve_css(css):
    '''
        serve_css

    '''
    return static_file(css, root='static/css/')

#-----------------------------------------------------------------------------

# Allow javascript
@route('/js/<js:path>')
def serve_js(js):
    '''
        serve_js

    '''
    return static_file(js, root='static/js/')

#-----------------------------------------------------------------------------
# Pages
#-----------------------------------------------------------------------------

# Redirect to login
@get('/home')
def get_index():
    '''
        get_index
        
        Serves the index page
    '''
    return model.index()

#-----------------------------------------------------------------------------

# Display the login page
@get('/login')
def get_login_controller():
    '''
        get_login
        
        Serves the login page
    '''
    return model.login_form()

#-----------------------------------------------------------------------------

# Attempt the login
@post('/login')
def post_login():
    '''
        post_login
        
        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    '''

    # Handle the form processing
    username = request.forms.get('username')
    password = request.forms.get('password')
    
    # Call the appropriate method
    return model.login_check(username, password)

#-----------------------------------------------------------------------------
# register a new user
#-----------------------------------------------------------------------------

@get('/about')
def get_about():
    '''
        get_about
        
        Serves the about page
    '''
    return model.about()

#-----------------------------------------------------------------------------

# Help with debugging
@post('/debug/<cmd:path>')
def post_debug(cmd):
    return model.debug(cmd)

#-----------------------------------------------------------------------------

# 404 errors, use the same trick for other types of errors
@error(404)
def error(error): 
    return model.handle_errors(error)
    
    
#-----------------------------------------------------------------------------

# bind fn. to get the contact page
@get('/contact')
def get_contact():
    return model.get_contact()


#-----------------------------------------------------------------------------

@get('/')
@get('/register')
def get_register():
    return model.get_register()

#-----------------------------------------------------------------------------

@post('/register')
def post_register():
    # Handle the form processing
    username = request.forms.get('username')
    password = request.forms.get('password')

    # usr public key -- pass this off to model.register_user
    pub_key = request.forms.get('pub_id')

    # Call the appropriate method
    return model.register_user(username, password, pub_key)

#-----------------------------------------------------------------------------


@get('/logout')
def logout():
	return model.logout()

#-----------------------------------------------------------------------------

@get('/users')
def get_users():
    # returns the page of the users
    # currently stored in the system
    # which aren't an admin
    return model.get_users()


# handle post-request from users
@post('/users')
def get_users():
	user = request.forms.get('message')

	print(user)

	return model.post_users(user)

#-----------------------------------------------------------------------------

# get message ciphertext & insert as row
# into the Message table in database.db
@post('/message')
def get_message_ciphertext():

    hmac = request.forms.get('hmac')
    cipher = request.forms.get('ciphertext')
    recipient = request.forms.get('recipient')
    pub_key = request.forms.get('sender_pub_key')
    nonce = request.forms.get('nonce')
    sender = request.forms.get('sender')

    print(cipher, '\n', recipient, '\n', pub_key, '\n', nonce, '\n', sender, sep='')

    return model.insert_msg_ciphertext(
        hmac = hmac,
		sender_pub_key = pub_key,
		ciphertext = cipher,
		recipient = recipient,
		nonce = nonce,
		sender = sender
	)









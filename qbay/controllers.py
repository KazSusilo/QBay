from qbay import database
from qbay.user import User
from qbay.database import app
from qbay.listing import Listing
from qbay.booking import Booking
from flask import render_template, request, session, redirect
from functools import wraps


def authenticate(inner_function):
    """
    :param inner_function: any python function that accepts a user object
    Wrap any python function and check the current session to see if 
    the user has logged in. If login, it will call the inner_function
    with the logged in user object.
    To wrap a function, we can put a decoration on that function.
    Example:
    @authenticate
    def home_page(user):
        pass
    """

    @wraps(inner_function)
    def wrapped_inner():
        # check did we store the key in the session
        if 'logged_in' in session:
            id = session['logged_in']
            try:
                # This generates a new User object that can interact with
                # the database via some tethering.
                # You want to use this object to pass around the program as it
                # has the needed functions for actually managing the database
                user = User.query_user(id)
                if user:
                    # if the user exists, call the inner_function
                    # with user as parameter
                    return inner_function(user)
                return redirect('/login')
            except Exception:
                pass
        else:
            # else, redirect to the login page
            return redirect('/login')

    # return the wrapped version of the inner_function:
    return wrapped_inner


@app.route('/')
@authenticate
def home(user):
    listings = database.Listing.query.all()
    return render_template('index.html', user=user, listings=listings)


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html', message='')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = User.login(email, password)
    except ValueError as err:
        return render_template('login.html', message=err, prevEmail=email)

    if user:
        session['logged_in'] = user.id
        """
        Session is an object that contains sharing information 
        between a user's browser and the end server. 
        Typically it is packed and stored in the browser cookies. 
        They will be past along between every request the browser made 
        to this services. Here we store the user object into the 
        session, so we can tell if the client has already login 
        in the following sessions.
        """
        # success! go back to the home page
        # code 303 is to force a 'GET' request
        return redirect('/', code=303)
    else:
        return render_template('login.html', message='login failed', 
                               prevEmail=email)


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
    return redirect('/')


@app.route('/register', methods=['GET'])
def register_get():
    # templates are stored in the templates folder
    return render_template('register.html', message='')


@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    error_message = None

    if password != password2:
        error_message = "The passwords do not match"
    else:
        # use backend api to register the user
        success = User.register(username, email, password)
        if not success:
            error_message = "Registration failed"
    # if there is any error messages when registering new user
    # at the backend, go back to the register page.
    if error_message:
        return render_template('register.html', message=error_message, 
                               prevEmail=email, prevUsername=username)
    else:
        return redirect('/login')


@app.route('/user_update', methods=['GET'])
@authenticate
def update_informations_get(user: User):
    return render_template('/user_update.html', user=user, errors='', 
                           prevEmail=user.email, prevUsername=user.username, 
                           prevBillingAddress=user.billing_address, 
                           prevPostalCode=user.postal_code)


@app.route('/user_update', methods=['POST'])
@authenticate
def update_informations_post(user: User):
    """Update the user information from the HTML page
    and push it onto the database
    """
    username = request.form.get('username')
    email = request.form.get('email')
    billing_address = request.form.get('billing_address')
    postal_code = request.form.get('postal_code')

    messages = []

    if user.email != email:
        try:
            user.update_email(email)
            messages += [f"Email updated successfully: {email}"]
        except ValueError as e:
            messages += [str(e)]

    if user.username != username:
        try:
            user.update_username(username)
            messages += [f"Username updated successfully: {username}"]
        except ValueError as e:
            messages += [str(e)]

    if user.billing_address != billing_address:
        try:
            user.update_billing_address(billing_address)
            messages += [
                f"Billing address updated successfully: {billing_address}"]
        except ValueError as e:
            messages += [str(e)]

    if user.postal_code != postal_code:
        try:
            user.update_postal_code(postal_code)
            messages += [f"Postal code updated successfully: {postal_code}"]
        except ValueError as e:
            messages += [str(e)]
    
    database.db.session.commit()

    return render_template('/user_update.html', user=user, errors=messages, 
                           prevEmail=user.email, prevUsername=username, 
                           prevBillingAddress=billing_address, 
                           prevPostalCode=postal_code)


@app.route('/booking/<int:listing_id>', methods=['GET'])
def booking_get(listing_id):
    listing = database.Listing.query.filter_by(id=listing_id).first()
    listing_obj = Listing.query_listing(listing_id)
    user = database.User.query.filter_by(id=session["logged_in"]).first()
    min_date = listing_obj.find_min_booking_date()
    return render_template('booking.html', listing=listing, user=user, 
                           min_date=min_date, message='')


@app.route('/booking/<int:listing_id>', methods=['POST'])
def booking_post(listing_id):
    user = database.User.query.filter_by(id=session["logged_in"]).first()
    buyer = user.id
    listing = database.Listing.query.filter_by(id=listing_id).first()
    listing_obj = Listing.query_listing(listing_id)
    seller = listing.owner_id
    start_date = request.form.get('trip-start')
    end_date = request.form.get('trip-end')
    
    try:
        Booking.book_listing(buyer, seller, listing_id, start_date, end_date)
        message = "Booking Successful: " + start_date + " to " + end_date
    except ValueError as e:
        message = str(e)
    min_date = listing_obj.find_min_booking_date()

    return render_template('booking.html', listing=listing, user=user, 
                           min_date=min_date, message=message)


@app.route('/user_bookings')
@authenticate
def view_user_bookings(user):
    listings = []
    bookings = database.Booking.query.filter_by(buyer_id=user.id).all()
    for booking in bookings:
        listing = database.Listing.query.get(booking.listing_id)
        listings.append(listing)

    return render_template('user_bookings.html', bookings=bookings, 
                           listings=listings)


@app.route('/create_listing', methods=['GET'])
def create_listing_get():
    return render_template('create_listing.html', message='')


@app.route('/create_listing', methods=['POST'])
@authenticate
def create_listing_post(user):
    title = request.form.get('title')
    description = request.form.get('description')
    price = float(request.form.get('price'))
    address = request.form.get('address')
    
    try:
        Listing.create_listing(title, description, price, user, address)
        database.db.session.commit()
    except ValueError as e:
        return render_template('create_listing.html', message=str(e), 
                               prevTitle=title, prevDescription=description, 
                               prevPrice=price, prevAddress=address)
    except TypeError as e:
        return render_template('create_listing.html', message=str(e), 
                               prevTitle=title, prevDescription=description, 
                               prevPrice=price, prevAddress=address)

    return redirect('/')


@app.route('/user_listings')
@authenticate
def view_user_listings(user):
    listings = database.Listing.query.filter_by(owner_id=user.id).all()
    return render_template('user_listings.html', listings=listings)


@app.route('/update_listing/<int:listing_id>', methods=['GET'])
def update_listing_get(listing_id):
    listing = database.Listing.query.get(listing_id)
    user = database.User.query.filter_by(id=session["logged_in"]).first()
    return render_template('/update_listing.html',
                           user=user, listing=listing, errors='',
                           prevTitle=listing.title, 
                           prevDescription=listing.description,
                           prevPrice=listing.price, 
                           prevAddress=listing.address)


@app.route('/update_listing/<int:listing_id>', methods=['POST'])
def update_listing_post(listing_id):
    listing = Listing.query_listing(listing_id)  # Listing obj linked to db obj
    title = request.form.get('title')
    description = request.form.get('description')
    price = float(request.form.get('price')) * 100
    address = request.form.get('address')

    messages = []
    if title != listing.title:
        try:
            listing.update_title(title)
            messages += [f"Title updated successfully: {title}"]
        except ValueError as e:
            messages += [str(e)]

    if description != listing.description:
        try:
            listing.update_description(description)
            messages += [f"Description updated successfully: {description}"]
        except ValueError as e:
            messages += [str(e)]

    if price != listing.database_obj.price:
        try:
            listing.update_price(price / 100)
            messages += [
                f"Price updated successfully: {price / 100:.2f}"]
        except ValueError as e:
            messages += [str(e)]

    if address != listing.database_obj.address:
        try:
            listing.update_address(address)
            messages += [f"Address updated successfully: {address}"]
        except ValueError as e:
            messages += [str(e)]

    database.db.session.commit()

    return render_template('/update_listing.html',
                           listing=listing.database_obj, messages=messages,
                           prevTitle=title, prevDescription=description, 
                           prevPrice=price, prevAddress=address)
    
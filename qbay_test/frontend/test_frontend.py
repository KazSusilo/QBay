from seleniumbase import BaseCase
from qbay.database import app, db
from qbay.user import User
from qbay_test.conftest import base_url
from unittest.mock import patch
from datetime import datetime

"""
This file defines all Front-end Integration Tests
"""


class FrontEndTests(BaseCase):
    def initialize_database(self):
        # Clear database
        with app.app_context():
            db.drop_all()
            db.create_all()

    def register_helper(self, email, username, password):
        # Register user given email, username, password
        self.open(base_url + '/register')
        self.type("#email", email)
        self.type("#username", username)
        self.type("#password", password)
        self.type("#password2", password)
        self.click('input[type="submit"]')

    def login_helper(self, email, password):
        # Log-in given email, password
        self.open(base_url + '/login')
        self.type("#email", email)
        self.type("#password", password)
        self.click('input[type="submit"]')

    def create_listing_helper(self, title, description, price, address):
        # Create listing given title, description, price
        self.click_link("Create Listing")
        self.type("#title", title)
        self.type("#description", description)
        self.type("#price", price)
        self.type("#address", address)
        self.click('input[type="submit"]')

    def update_listing_helper(self, title, description, price):
        # Update listing given title, description, price
        self.click_link("My Listings")
        self.click_link("Edit")
        self.type("#title", title)
        self.type("#description", description)
        self.type("#price", price)
        self.click('input[type="submit"]')

    def booking_helper(self, start_date, end_date):
        # Book listing given a start_date and end_date
        self.click_link("Book")
        self.type("#start", start_date)
        self.type("#end", end_date)
        self.click('input[type="submit"]')

    def assert_helper(self, element, text, url):
        # Assert given an element, text, and return to desired url
        self.assert_element(element)
        self.assert_text(text, element)
        if (url):
            self.open(url)

    

    def test_booking(self, *_):
        # Initialize database
        self.initialize_database()

        # Register & Log-in
        email, username = "booklisting01@test.com", "Book Listing 01"
        password = "Onetwo!"
        self.register_helper(email, username, password)
        self.login_helper(email, password)

        # Create listing
        t, d, p = "6 Bed 9 Bath", "This is a lovely place", 100
        a = "101 Palace Place, Suite 330, Boston, MA"
        self.create_listing_helper(t, d, p, a)

        # Book as owner of listing
        self.booking_helper("2025-01-01", "2025-01-02")
        element, text = "#message", "Owner and buyer are the same!"
        self.assert_helper(element, text, None)

        # Register & Log-in with new account
        self.open(base_url + "/logout")
        email, username = "booklisting02@test.com", "Book Listing 02"
        password = "Onetwo!"
        self.register_helper(email, username, password)
        self.login_helper(email, password)

        # Book with same dates 
        self.booking_helper("2025-01-01", "2025-01-01")
        text = "Start date is same or after end date!"
        self.assert_helper(element, text, base_url)

        # Book with start date after end date
        self.booking_helper("2025-01-02", "2025-01-01")
        self.assert_helper(element, text, base_url)

        # Book with invalid balance
        self.booking_helper("2024-12-31", "2025-01-02")
        text = "Buyer's balance is too low for this booking!"
        self.assert_helper(element, text, base_url)

        # Book with valid dates & balance
        self.booking_helper("2025-01-01", "2025-01-02")
        text = "Booking Successful: 2025-01-01 to 2025-01-02"
        self.assert_helper(element, text, None)
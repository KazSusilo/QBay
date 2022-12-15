import unittest
from qbay.database import app, db
from qbay.user import User
from qbay.listing import Listing
from qbay.booking import Booking
from datetime import datetime, timedelta

"""
This file defines all SQL Injection Back-end Tests
"""

ctx = app.app_context()
ctx.push()


class UnitTest(unittest.TestCase):
    def test_username(self):
        """ 
        For each line/input/test-case, pass through the User.register() 
        function as the username parameter to test for vulnerabilities
        """
        with open("./qbay_test/Generic_SQLI.txt") as f:
            for line in f:
                User.register(line, "testemail@gmail.com",
                              "Pass123!!")

    def test_email(self):
        """ 
        For each line/input/test-case, pass through the User.register() 
        function as the email parameter to test for vulnerabilities
        """
        with open('./qbay_test/Generic_SQLI.txt') as f:
            for line in f:
                User.register("Bob", line, "Pass123!!")

    def test_password(self):
        """ 
        For each line/input/test-case, pass through the User.register() 
        function as the password parameter to test for vulnerabilities
        """
        with open('./qbay_test/Generic_SQLI.txt') as f:
            for line in f:
                User.register("Bob", "testemail@gmail.com", line)

    def create_account(self, username, email, password):
        """Create account to verify in test_create_listing functions"""
        # Create account
        User.register(username, email, password)
        return User.login(email, password)

    def test_create_listing_title_injection(self):
        """
        For each line/input/test-case, pass through the Listing.create_listing
        function as the title parameter to test for vulnerabilities
        """
        username, email, password = "TestCL1", "testCL1@gmail.com", "Onetwo!"
        account = self.create_account(username, email, password)
        title, description, price = "", "This is a lovely place", 100
        with open('./qbay_test/Generic_SQLI.txt') as f:
            for line in f:
                try:
                    # Parameter changed
                    title = line
                    Listing.create_listing(title, description, price, account)
                except ValueError as e:
                    assert str(e) == "Invalid Title: " + line

    def test_create_listing_description_injection(self):
        """
        For each line/input/test-case, pass through the Listing.create_listing
        function as the description parameter to test for vulnerabilities
        """
        username, email, password = "TestCL2", "testCL2@gmail.com", "Onetwo!"
        account = self.create_account(username, email, password)
        title, description, price = "Place x", "", 100
        with open('./qbay_test/Generic_SQLI.txt') as f:
            i = 1
            for line in f:
                try:
                    # Parameters changed
                    title, description, i = "Place " + str(i), line, i + 1
                    Listing.create_listing(title, description, price, account)
                except ValueError as e:
                    assert str(e) == "Invalid Description: " + line

    def test_create_listing_price_injection(self):
        """
        For each line/input/test-case, pass through the Listing.create_listing
        function as the price parameter to test for vulnerabilities
        """
        username, email, password = "TestCL3", "testCL3@gmail.com", "Onetwo!"
        account = self.create_account(username, email, password)
        title, description, price = "House x", "This is a lovely place", 0
        with open('./qbay_test/Generic_SQLI.txt') as f:
            i = 1
            for line in f:
                try:
                    # Parameter changed
                    title, price, i = "House " + str(i), float(line), i + 1
                    Listing.create_listing(title, description, price, account)
                except ValueError as e:
                    # Check if error is of type 1 or type 2
                    try:
                        # Type 1: line cannot be converted to float
                        assert (str(e)[0:33]) == ("could not convert " +
                                                  "string to float")
                    except AssertionError:
                        # Type 2: line is an invalid price
                        assert str(e) == "Invalid Price: " + str(price)

    def test_create_listing_seller_injection(self):
        """
        For each line/input/test-case, pass through the Listing.create_listing
        function as the seller parameter to test for vulnerabilities
        """
        account = None
        title, description, price = "Home x", "This is a lovely place", 10
        with open("./qbay_test/Generic_SQLI.txt") as f:
            i = 1
            for line in f:
                try:
                    # Parameter changed
                    title, account, i = "Home " + str(i), line, i + 1
                    Listing.create_listing(title, description, price, account)
                except AttributeError as e:
                    # AttributeError e should prints "Invalid attribute: id"
                    # e.name should be the same as the invalid attribute name"
                    assert e.name == 'id'

    def test_create_listing_address_injection(self):
        """
        For each line/input/test-case, pass through the Listing.create_listing
        function as the address parameter to test for vulnerabilities
        """
        username, email, password = "TestCL5", "testCL5@gmail.com", "Onetwo!"
        account = self.create_account(username, email, password)
        title, description, price = "Maison x", "This is a lovely place", 10
        with open("./qbay_test/Generic_SQLI.txt") as f:
            i = 0
            for line in f:
                # Parameter changed
                title, address, i = "Maison " + str(i), line, i + 1
                Listing.create_listing(title, description, price, account, 
                                       address)

    def initialize_database(self):
        """Clear database"""
        with app.app_context():
            db.drop_all()
            db.create_all()

    def booking_id_helper(self, buyer_id, owner_id, listing_id, type):
        test_id = -1
        
        start = datetime.strptime("2022-12-01", "%Y-%m-%d")
        end = datetime.strptime("2022-12-02", "%Y-%m-%d")
        with open("./qbay_test/Generic_SQLI.txt") as f:
            for line in f:
                try:
                    test_id = int(line)
                    if type == "Owner":
                        owner_id = test_id
                    elif type == "Buyer":
                        buyer_id = test_id
                    elif type == "Listing":
                        listing_id = test_id
                    Booking.book_listing(buyer_id=buyer_id,
                                         owner_id=owner_id,
                                         listing_id=listing_id,
                                         book_start=start,
                                         book_end=end)
                except ValueError as e:
                    try:
                        # Type 1: line cannot be converted to int
                        assert str(e) == ("invalid literal for int() with " +
                                          "base 10: " + repr(line))
                    except AssertionError:
                        # Type 2: line is an invalid ID
                        assert str(e) == ("Invalid " + type + " ID: " 
                                          + str(test_id))

    def booking_date_helper(self, buyer_id, owner_id, listing_id, type):
        start = datetime.strptime("2022-12-01", "%Y-%m-%d")
        end = datetime.strptime("2022-12-02", "%Y-%m-%d")
        form = "%Y-%m-%d"

        with open("./qbay_test/Generic_SQLI.txt") as f:
            for line in f:
                try:
                    test = datetime.strptime(line, "%Y-%m-%d")
                    if type == "Start":
                        start = test
                    elif type == "End":
                        end = test
                    Booking.book_listing(buyer_id=buyer_id,
                                         owner_id=owner_id,
                                         listing_id=listing_id,
                                         book_start=start,
                                         book_end=end)
                except ValueError as e:
                    # Type 1: line cannot be converted to datetime string
                    assert str(e) == ("time data " + repr(line) +
                                      " does not match format " + repr(form))
                                          
    def test_booking_buyer(self):
        """
        For each line/input/test-case, pass through the Booking.book_listing
        function as the buyer parameter to test for vulnerabilities
        """
        self.initialize_database()
        owner = self.create_account("testUser1", "user@test.ca", "Pass123!")
        listing = Listing.create_listing("4 bed 2 bath", 
                                         "Amazing and comfortable place",
                                         15.00, owner, "10 King St.")
        self.booking_id_helper(None, owner.id, listing.id, "Buyer")

    def test_booking_seller(self):
        """
        For each line/input/test-case, pass through the Booking.book_listing
        function as the seller parameter to test for vulnerabilities
        """
        with app.app_context():
            db.drop_all()
            db.create_all()

        owner = self.create_account("testUser", "user@example.ca", "Pass123!")
        listing = Listing.create_listing("4 bed 2 bath", 
                                         "Amazing and comfortable place",
                                         15.00, owner, "10 King St.")
        buyer = self.create_account("testUser2", "user2@test.ca", "Pass123!")

        self.booking_id_helper(buyer.id, None, listing.id, "Owner")

    def test_booking_listing(self):
        """
        For each line/input/test-case, pass through the Booking.book_listing
        function as the listing parameter to test for vulnerabilities
        """
        self.initialize_database()          
        owner = self.create_account("testUser", "user@example.ca", "Pass123!")
        buyer = self.create_account("testUser2", "user2@test.ca", "Pass123!")
        self.booking_id_helper(buyer.id, owner.id, None, "Listing")

    def test_booking_start_date(self):
        """
        For each line/input/test-case, pass through the Booking.book_listing
        function as the start_date parameter to test for vulnerabilities
        """
        self.initialize_database()
        owner = self.create_account("testUser", "user@example.ca", "Pass123!")
        listing = Listing.create_listing("4 bed 2 bath", 
                                         "Amazing and comfortable place",
                                         15.00, owner, "10 King St.")
        buyer = self.create_account("testUser2", "user2@test.ca", "Pass123!")
        self.booking_date_helper(buyer.id, owner.id, listing.id, "Start")

    def test_booking_end_date(self):
        """
        For each line/input/test-case, pass through the Booking.book_listing
        function as the end_date parameter to test for vulnerabilities
        """
        self.initialize_database()
        owner = self.create_account("testUser", "user@example.ca", "Pass123!")
        listing = Listing.create_listing("4 bed 2 bath", 
                                         "Amazing and comfortable place",
                                         15.00, owner, "10 King St.")
        buyer = self.create_account("testUser2", "user2@test.ca", "Pass123!")

        self.booking_date_helper(buyer.id, owner.id, listing.id, "End")
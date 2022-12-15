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
        """ For each line/input/test-case, pass through the 
        User.register() function as the username parameter to test for 
        vulnerabilities to SQL Injection
        """
        with open("./qbay_test/Generic_SQLI.txt") as f:
            for line in f:
                User.register(line, "testemail@gmail.com",
                              "Pass123!!")

    def test_email(self):
        """ For each line/input/test-case, pass through the 
        User.register() function as the email parameter to test for 
        vulnerabilities to SQL Injection
        """
        with open('./qbay_test/Generic_SQLI.txt') as f:
            for line in f:
                User.register("Bob", line, "Pass123!!")

    def test_password(self):
        """ For each line/input/test-case, pass through the 
        User.register() function as the password parameter to test for 
        vulnerabilities to SQL Injection
        """
        with open('./qbay_test/Generic_SQLI.txt') as f:
            for line in f:
                User.register("Bob", "testemail@gmail.com", line)

    """Create account to verify in test_create_listing functions"""

    def create_account(self, username, email, password):
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
        description, price = "This is a lovely place", 0
        with open('./qbay_test/Generic_SQLI.txt') as f:
            for line in f:
                cur = 0
                title = f"Testing title {cur}"
                try:
                    # Parameter changed
                    price = float(line)
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
                cur += 1

    def test_listing_inject_seller(self):
        """
        Attempt to pass in the injection text as plain string to the database
        Should catch attribute error when trying to parse the object
        """
        with app.app_context():
            db.drop_all()
            db.create_all()

        with open("./qbay_test/Generic_SQLI.txt") as f:
            cur = 0
            for line in f:
                title = f"Testing title {cur}"
                try:
                    Listing.create_listing(title=title,
                                           description="testing description 1",
                                           price=10.0,
                                           owner=line,
                                           address="101 Kingstreet"
                                           )
                except AttributeError as e:
                    # AttributeError e should prints "Invalid attribute: id"
                    # e.name should be the same as the invalid attribute name"
                    assert e.name == 'id'
                cur += 1

    def test_listing_inject_address(self):
        """
        Pass in injection string into database.
        String should be accepted but does not execute code
        """
        with app.app_context():
            db.drop_all()
            db.create_all()

        user = User("testUser", "user@example.ca", "Pass123!")
        user.add_to_database()

        with open("./qbay_test/Generic_SQLI.txt") as f:
            cur = 0
            for line in f:
                title = f"Testing title {cur}"
                Listing.create_listing(title=title,
                                       description="testing description 1",
                                       price=10.0,
                                       owner=user,
                                       address=line
                                       )
                cur += 1
    
    def create_listing_helper(self, title, description, price, owner, address):
        listing = Listing.create_listing(title, description, price,
                                         owner, address)
        return listing

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
                                          
    def test_booking_buyer(self):
        with app.app_context():
            db.drop_all()
            db.create_all()

        owner = self.create_account("testUser1", "user@test.ca", "Pass123!")
        listing = self.create_listing_helper("4 bed 2 bath", 
                                             "Amazing and comfortable place",
                                             15.00, owner, "10 King St.")
        self.booking_id_helper(None, owner.id, listing.id, "Buyer")

    def test_booking_seller(self):
        with app.app_context():
            db.drop_all()
            db.create_all()

        owner = self.create_account("testUser", "user@example.ca", "Pass123!")
        listing = self.create_listing_helper("4 bed 2 bath", 
                                             "Amazing and comfortable place",
                                             15.00, owner, "10 King St.")
        buyer = self.create_account("testUser2", "user2@test.ca", "Pass123!")

        self.booking_id_helper(buyer.id, None, listing.id, "Owner")

    def test_booking_listing(self):
        with app.app_context():
            db.drop_all()
            db.create_all()

        owner = self.create_account("testUser", "user@example.ca", "Pass123!")
        buyer = self.create_account("testUser2", "user2@test.ca", "Pass123!")
        self.booking_id_helper(buyer.id, owner.id, None, "Listing")

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

    def test_booking_start_date(self):
        with app.app_context():
            db.drop_all()
            db.create_all()

        owner = self.create_account("testUser", "user@example.ca", "Pass123!")
        listing = self.create_listing_helper("4 bed 2 bath", 
                                             "Amazing and comfortable place",
                                             15.00, owner, "10 King St.")
        buyer = self.create_account("testUser2", "user2@test.ca", "Pass123!")
        self.booking_date_helper(buyer.id, owner.id, listing.id, "Start")

    def test_booking_end_date(self):
        with app.app_context():
            db.drop_all()
            db.create_all()

        owner = self.create_account("testUser", "user@example.ca", "Pass123!")
        listing = self.create_listing_helper("4 bed 2 bath", 
                                             "Amazing and comfortable place",
                                             15.00, owner, "10 King St.")
        buyer = self.create_account("testUser2", "user2@test.ca", "Pass123!")

        self.booking_date_helper(buyer.id, owner.id, listing.id, "End")
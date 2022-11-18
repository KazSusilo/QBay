# listing.py
from enum import Enum, unique
from multiprocessing.sharedctypes import Value
from qbay import database
from qbay.database import db
from qbay.user import User
from qbay.review import Review
from datetime import datetime
import re


class Listing:
    """Object representation of a digital Listing

    params:
    REQUIRED
    - title: Title of listing (string)
    - description: A short description (string)
    - price: The cost of renting the listing (float)
    - date: The last modification date (date)
    - seller: The User associated with the listing (User)

    EXTRA
    - address: The location of the listing (string)
    - reviews: A list of reviews associates with the listing (list[Review])
    """

    """ Initialize digital Listing"""
    def __init__(self, title: str = "", description: str = "",
                 price: float = 0.0, owner: User = User(), address: str = ""):
        # Required
        self._database_obj: database.Listing = None
        self._id = None
        self._title = title
        self._description = description
        self._price = price
        self._created_date: datetime = datetime.now()
        self._modified_date: datetime = datetime.now()
        self._seller = owner

        # Extra
        self._address: str = address
        self._reviews: list[Review] = []

    # Required
    """Fetches title of digital Listing"""
    @property
    def title(self):
        if self.database_obj:
            self._title = self.database_obj.title
        return self._title

    """Sets title for digital Listing if valid"""
    @title.setter
    def title(self, title):
        if not (Listing.valid_title(title)):
            raise ValueError(f"Invalid Title: {title}")
        self._title = title
        self._modified_date = datetime.now()

    """Fetches description of digital Listing"""
    @property
    def description(self):
        if self.database_obj:
            self._description = self.database_obj.description
        return self._description

    """Sets title for digital Listing if valid"""
    @description.setter
    def description(self, description):
        if not ((20 <= len(description) <= 2000)
                and (len(description) > len(self.title))):
            raise ValueError(f"Invalid Description: {description}")
        self._description = description
        self._modified_date = datetime.now()

    """Fetches price of digital Listing"""
    @property
    def price(self):
        if self.database_obj:
            self._price = self.database_obj.price / 100
        return self._price

    """Sets price for digital Listing if valid"""
    @price.setter
    def price(self, price):
        if not (Listing.valid_price(price) and self.price < price):
            raise ValueError(f"Invalid Price: {price}")
        self._price = price
        self._modified_date = datetime.now()

    """Fetches last modification date of digital listing"""
    @property
    def created_date(self):
        if self.database_obj:
            self.created_date = self.database_obj.time_created
        return self._created_date

    """Fetches last date modified"""
    @property
    def modified_date(self):
        if self.database_obj:
            self._modified_date = self.database_obj.last_modified_date
        return self._modified_date.date().isoformat()

    """Fetches owner of digital Listing"""
    @property
    def seller(self):
        return self._seller

    """Sets owner of digital Listing if valid"""
    @seller.setter
    def seller(self, owner):
        if (not Listing.valid_seller(owner)):
            raise ValueError(f"Invalid Seller: {owner}")
        self._seller = owner
        self._modified_date = datetime.now()

    # Extra
    """Fetches address of Listing"""
    @property
    def address(self):
        return self._address

    """Sets address of Listing"""
    @address.setter
    def address(self, location):
        self._address = location
        self._modified_date = datetime.now()

    """Fetches reviews of Listing"""
    @property
    def reviews(self) -> 'list[Review]':
        return self._reviews

    """Sets reviews of Listing"""
    @reviews.setter
    def reviews(self, comments: 'list[Review]'):
        self._reviews = comments
        self._modified_date = datetime.now()

    """Add reviews to listing"""
    def add_review(self, review: 'Review'):
        self._reviews.append(review)
        # note: adding a review will currently not update the
        # last_modified_date, since it's not modifying the actual post

    # Database
    """Returns a reference to the database"""
    @property
    def database_obj(self) -> database.Listing:
        return self._database_obj

    """Fetches the user's id"""
    @property
    def id(self):
        if self.database_obj:
            self._id = self.database_obj.id
        return self._id

    """Adds listing to the database"""
    def add_to_database(self):
        listing = database.Listing(title=self.title,
                                   description=self.description,
                                   price=self.price * 100,
                                   owner_id=self.seller.id,
                                   last_modified_date=self.modified_date)
        with database.app.app_context():
            db.session.add(listing)
            db.session.commit()
            self._database_obj = listing
            self._modified_date = listing.last_modified_date
            self._id = listing.id

    @staticmethod
    def create_listing(title, description, price, owner):
        """Creates new listing
        Client can not modify the mod_date, rather, it is handled in the 
        server database upon entry update 

        params:
        - title: Title of listing (string)
        - description: A short description (string)
        - price: The cost of renting the listing (float)
        - owner: The User associated with the listing (User)

        """
        if not (Listing.valid_title(title)):
            raise ValueError(f"Invalid Title: {title}")
        if not (Listing.valid_description(description, title)):
            raise ValueError(f"Invalid Description: {description}")
        if not (Listing.valid_price(price)):
            raise ValueError(f"Invalid Price: {price}")
        if not (Listing.valid_seller(owner)):
            raise ValueError(f"Invalid Seller: {owner}")
            
        listing = Listing(title, description, price, owner)
        listing.add_to_database()
        return listing

    @staticmethod
    def query_listing(id):
        """Returns a Listing object for interacting with the database
        in a safe manner. It will initialize a new User object that
        is tethered to the corresponding database object

        Args:
            id (int): integer denoting the unique identifier of the object
            to be queried for

        Returns:
            Listing: a listing object that is tethered to the corresponding
            database object with the given id
        """
        database_listing = database.Listing.query.get(int(id))
        if database_listing:
            listing = Listing()
            listing._database_obj = database_listing
            return listing
        return None

    # Validation Functions
    """Determine if a given title is valid """
    @staticmethod
    def valid_title(title):
        regex = re.compile(
            r'(^([A-Za-z0-9]([A-Za-z0-9]| ){,78}[A-Za-z0-9])$)|[A-Za-z0-9]')
        if re.fullmatch(regex, title):
            with database.app.app_context():
                exists = database.Listing.query.filter_by(title=title).all()
            return not len(exists)
        return False

    """Determine if a given description is valid"""
    @staticmethod
    def valid_description(description, title):
        return ((19 < len(description) < 2001)
                and (len(title) < len(description)))

    """Determine if a given price is valid"""
    @staticmethod
    def valid_price(price):
        return (10.00 <= price <= 10000.00)

    """Determine if a given last modification date is valid"""
    @staticmethod
    def valid_date(mod_date):
        min_date = datetime(2021, 1, 2)
        max_date = datetime(2025, 1, 2)
        return (min_date < mod_date < max_date)

    """Determine if a given owner is valid"""
    @staticmethod
    def valid_seller(owner):
        if (owner.id):
            with database.app.app_context():
                user = database.User.query.get(owner.id)
                return ((user is not None) and (user.email != ""))
        return False
    
    """Updates the listing title and pushes changes to the database"""
    def update_title(self, title):
        self.title = title
        with database.app.app_context():
            self.database_obj.title = title
            db.session.commit()
    
    """Updates the listing description and pushes changes to the database"""
    def update_description(self, description):
        self.description = description
        with database.app.app_context():
            self.database_obj.description = description
            db.session.commit()

    """Updates the listing price and pushes changes to the database"""
    def update_price(self, price):
        self.price = price
        with database.app.app_context():
            self.database_obj.price = price * 100
            db.session.commit()
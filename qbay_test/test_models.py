import unittest

from qbay.review import Review
from qbay.user import User
from qbay.listing import Listing
from qbay.transaction import Transaction, TransactionStatus
from qbay.wallet import Wallet, BankingAccount


class UnitTest(unittest.TestCase):

    def test_user(self):
        user = User()

        user.id = 10
        assert user.id == 10

        user.username = "KanchShres"
        assert user.username == "KanchShres"

        user.email = "19ks62@queensu.ca"
        assert user.email == "19ks62@queensu.ca"

        user.password = "password123"
        assert user.password == "password123"

        test_wall = Wallet()
        user.wallet = test_wall
        assert user.wallet == test_wall

        test_rev = Review()
        user.add_review(test_rev)
        assert user.reviews[0] == test_rev

    def test_review(self):
        review = Review()

        review.id = 1
        assert review.id == 1

        review.date_posted = "September 21, 2022"
        assert review.date_posted == "September 21, 2022"

        test_user = User()
        review.posting_user = test_user
        assert review.posting_user == test_user

        test_listing = Listing()
        review.listing = test_listing
        assert review.listing == test_listing

        review.rating = 3.4
        assert review.rating == 3.4

        review.comment = "hello world"
        assert review.comment == "hello world"

    def test_wallet_balance_transfer(self):
        bank_account = BankingAccount()
        user = User()
        wallet = user.create_wallet()
        user.wallet.bankingAccount = bank_account

        bank_account.add_balance(10000)
        assert user.wallet.bankingAccount.balance == 10000
        assert user.wallet.balance == 0

        user._wallet.transfer_balance(4000)
        assert user.wallet.bankingAccount.balance == 6000
        assert user.balance == 4000
        assert wallet.balance == 4000

        with self.assertRaises(ValueError):
            user.wallet.transfer_balance(-2000)
        
        with self.assertRaises(ValueError):
            bank_account.add_balance(-2000)

        assert user.balance == 4000
        assert bank_account.balance == 6000

    def test_transaction(self):
        transact = Transaction()
        transact.id = 50
        assert transact.id == 50

        test_user = User()
        transact.payer = test_user
        assert transact.payer == test_user

        test_user_2 = User()
        transact.payee = test_user_2
        assert transact.payee == test_user_2

        transact.amount = 50
        assert transact.amount == 50
        
        test_listing = Listing()
        transact.listing = test_listing
        assert transact.listing == test_listing

        transact.status = "transactionInProgress"
        assert transact.status == TransactionStatus.IN_PROGRESS

    def test_transaction_invalid_status(self):
        transact = Transaction()
        transact.status = TransactionStatus.COMPLETED
        assert transact.status == TransactionStatus.COMPLETED

        transact.status = "transactionCancelled"
        assert transact.status == TransactionStatus.CANCELLED

        with self.assertRaises(ValueError):
            transact.status = "Value error"
        
        with self.assertRaises(TypeError):
            transact.status = None

        with self.assertRaises(TypeError):
            transact.status = User()

    def test_listing(self):
        # Testing Initialization
        obj = Listing()
        # Testing param manipulation #
        obj.title = "4 Bed 2 Bath"
        obj.address = "Queen's University"
        obj.price = 8000.57
        obj._description = "Shittiest school to ever exist"
        obj.seller.username = "bob"
        r = []
        r1 = Review()
        r.append(r1)
        obj.reviews = r
        r2 = Review()
        obj.add_review(r2)
        
        assert obj.title == "4 Bed 2 Bath"
        assert obj.price == 8000.57
        assert obj.address == "Queen's University"
        assert obj._description == "Shittiest school to ever exist"
        assert obj.seller.username == "bob"
        assert obj.reviews == [r1, r2]


def test_r5_1_update_listing():
    """ Testing R5-1:
    One can update all attributes of the listing, except 
    owner_id and last_modified_date.
    """
    # Initialize Listing
    obj = Listing()
    obj.title = "4 Bed 2 Bath"
    obj.address = "Queen's University"
    obj.price = 8000.57
    obj._description = "Shittiest school to ever exist"
    obj.seller.username = "bob"

    reviews = []
    r1 = Review()
    reviews.append(r1)
    obj.reviews = reviews
    r2 = Review()
    obj.add_review(r2)

    # test if changing the title works
    obj.update_title("different title")
    assert obj.title == "different title"

    # test if chaning the address works
    obj.update_address("different address")
    assert obj.address == "different address"

    # test if changing the price works (not testing R5-3 yet)
    obj.update_price(8100)
    assert obj.price == 8100

    obj.update_description("different description")
    assert obj.description == "different description"

    old_seller_id = obj.seller_id
    obj.udpate_seller_id(123)
    assert obj.seller_id == old_seller_id

    old_reviews = obj.reviews
    r1 = Review()
    obj.add_review(r1)
    assert obj.reviews == old_reviews.append(r1)

    


def test_r5_2_update_listing():
    """ Testing R5-2:
    Price can be only increased but cannot be decreased.
    """
    # Initialize listing
    obj = Listing()

    # make sure price does not change, as change is invalid
    obj.update_price(8100)
    obj.update_price(1500)
    assert obj.price == 8100

    # make sure price does change, as change is valid
    obj.update_price(8200)
    assert obj.price == 8200

def test_r5_3_update_listing():
    """ Testing R5-3:
    last_modified_date should be updated when the update operation 
    is successful.
    """
    # Initialize listing
    obj = Listing()

    old_last_modified_date = obj.last_modified_date
    obj.update_description("new description")
    assert obj.last_modified_date > old_last_modified_date

def test_r5_4_update_listing():
    """ Testing R5-4:
    When updating an attribute, one has to make sure that it follows 
    the same requirements as above. Mainly the subsections of R4.
    """
    # Copy and modify test cases for R4-1 through R4-8.
    # Modify so updating instead of creating.
    # Waiting on completion create listing test cases.

if __name__ == "__main__":
    unittest.main()

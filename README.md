[![Pytest-All](https://github.com/KazSusilo/QBay/actions/workflows/pytest-all.yml/badge.svg?branch=main)](https://github.com/kanchshres/C327-Group-12/actions/workflows/pytest-all.yml)
[![Python PEP8](https://github.com/KazSusilo/QBay/actions/workflows/style_checker.yml/badge.svg?branch=main)](https://github.com/KazSusilo/QBay/actions/workflows/pytest-all.yml)


# QBay
![HomePageLotsListings](https://user-images.githubusercontent.com/97570310/208317875-fbefdadd-2b07-4e6f-b919-fb81211c5db4.png)


## Summarry
QBay is a Web-Application, similar to Airbnb, for Client-to-Client vacation house rentals focused on short-term homestays and experiences. Rewarded with a $100 Sign-Up Bonus, users are able to view and book a variety of listings offered by their fellow users. In addition, users are also able to create their own listings for others to enjoy!

## Run-Instructions
### Python-Option
Along with Python, the following dependencies are required to run the application:
```
Flask
Flask-SQLAlchemy
pymysql
```
To install, run the command `pip install -r requirements.txt` from the root-directory `QBay`. Once the dependencies are installed, use command `python -m qbay` to run the application which can then be accessed with the following [link](http://127.0.0.1:8081).


### Docker-Option
After installing [docker](https://docs.docker.com/get-docker/), run the following command from the directory `QBay/docker` and open the website with the following [link](http://0.0.0.0:8081).
```
docker-compose up
```

## Features
### Login / Register
Initially, users are brought to the `Login` page where they can use their registed Email and Password to login. If they have yet register, they can do so by clicking the "Register" button, which will redirect them to the `Register` page.

![LoginPage](https://user-images.githubusercontent.com/97570310/208318802-59cc97d5-2094-49cd-a6a0-0731a7f24c60.png)
![RegisterPage](https://user-images.githubusercontent.com/97570310/208318803-7d402117-78de-4191-af74-984b3e8c0bce.png)


### Home
Once users have registered and logged-in, they will be presented with the `Home` page. At the top of the screen, they are greeted with a welcome message followed by their current balance. 

Slightly below the current balance, users are presented with four buttons including the "My Profile", "My Listings", "My Bookings", and "Create Listing" that redirect them to their corresponding pages. 

Under the "Listings" header, they will find all the available listings created by users, including the details of the listings and its corresponding "Book" button if they are interested in a rental.

Finally, the user can logout of their account by clicking the "Logout" button located at the top right corner.

![HomePage](https://user-images.githubusercontent.com/97570310/208318103-3369244d-d498-4c4d-9d7f-bd28917fe70c.png)

### Booking
Clicking the "Book" button corresponding to the desired listing on the `Home` page, the user is presented with the `Booking` page. Here the user can view the details of the listing as well as select their desired rental period. 

![BookingPage](https://user-images.githubusercontent.com/97570310/208318402-2714afed-60bf-40d5-ba47-3be468cf71dc.png)


### Edit Profile
Clicking the "My Profile" button on the `Home` page, the user is presented with the `Update User Page`. Here the user can udate their profile fields such as their email, username, billing address, and postal code. 

![EditProfilePage](https://user-images.githubusercontent.com/97570310/208318473-6bd333aa-f145-4270-af32-dc25c603bbff.png)


### My Listings
Clicking the "My Listings" button on the `Home` page, the user is presented with the `My Listings` page. Here the user can view/edit their created listings. To edit a listing, simply click the "Edit" button corresponding to the desired listing to be redirected to the `Update Listing` page. 

![MyListingsPage](https://user-images.githubusercontent.com/97570310/208318345-e364ccf4-cecc-42a0-966a-f63c35feb200.png)
![EditListingPage](https://user-images.githubusercontent.com/97570310/208318346-d673e8ee-17bc-4214-b2fa-04756496de8d.png)


### My Bookings
Clicking the "My Bookings" button on the `Home` page, the user is presented with the `My Bookings` page. Here the user can view their booked listings, including the details of the listing as well as their booked rental period.

![MyBookingsPage](https://user-images.githubusercontent.com/97570310/208318824-481c2d9d-c17c-4db7-9e89-0696a9b879be.png)


### Create Listing
Clicking the "Create Listings" button on the `Home` page, the user is presented with the `Create Listing` page. Here the user can create their own listing by filling out fields such as the title, description, price, and address.

![CreateListingPage](https://user-images.githubusercontent.com/97570310/208318110-1530218a-62f8-44da-83d6-febcfb430657.png)

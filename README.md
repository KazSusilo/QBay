[![Pytest-All](https://github.com/KazSusilo/QBay/actions/workflows/pytest-all.yml/badge.svg?branch=main)](https://github.com/kanchshres/C327-Group-12/actions/workflows/pytest-all.yml)
[![Python PEP8](https://github.com/KazSusilo/QBay/actions/workflows/style_checker.yml/badge.svg?branch=main)](https://github.com/KazSusilo/QBay/actions/workflows/pytest-all.yml)


# QBay
![HomePageListings](https://user-images.githubusercontent.com/97570310/208280289-b8c5fd70-1f11-4e72-b531-4b9a8c48b4b4.png)


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

![LoginPage](https://user-images.githubusercontent.com/97570310/208280109-aa685f2f-b68d-47bf-8f40-c5f2bd68b42c.png)
![RegisterPage](https://user-images.githubusercontent.com/97570310/208280112-572fabe2-9408-44f9-a991-d5239a9e3b93.png)


### Home
Once users have registered and logged-in, they will be presented with the `Home` page. At the top of the screen, they are greeted with a welcome message followed by their current balance. 

Slightly below the current balance, users are presented with four buttons including the "My Profile", "My Listings", "My Bookings", and "Create Listing" that redirect them to their corresponding pages. 

Under the "Listings" header, they will find all the available listings created by users, including the details of the listings and its corresponding "Book" button if they are interested in a rental.

Finally, the user can logout of their account by clicking the "Logout" button located at the top right corner.

![HomePageListings](https://user-images.githubusercontent.com/97570310/208280245-cd075e19-ce2a-45a4-87d7-429944e11f87.png)

### Booking
Clicking the "Book" button corresponding to the desired listing on the `Home` page, the user is presented with the `Booking` page. Here the user can view the details of the listing as well as select their desired rental period. 

![BookingPage](https://user-images.githubusercontent.com/97570310/208283238-99bbb9ca-5b70-441d-97fe-607ffdfd33e9.png)


### Edit Profile
Clicking the "My Profile" button on the `Home` page, the user is presented with the `Update User Page`. Here the user can udate their profile fields such as their email, username, billing address, and postal code. 

![EditProfilePage](https://user-images.githubusercontent.com/97570310/208282677-bb789278-a4b8-418f-9348-df9ae556e50e.png)


### My Listings
Clicking the "My Listings" button on the `Home` page, the user is presented with the `My Listings` page. Here the user can view/edit their created listings. To edit a listing, simply click the "Edit" button corresponding to the desired listing to be redirected to the `Update Listing` page. 

![MyListingsPage](https://user-images.githubusercontent.com/97570310/208282935-4e0df06b-acba-45ec-9a66-6e735ff2e6f7.png)
![EditListingPage](https://user-images.githubusercontent.com/97570310/208282937-2cdea973-430d-4638-9599-c842e00e4d97.png)


### My Bookings
Clicking the "My Bookings" button on the `Home` page, the user is presented with the `My Bookings` page. Here the user can view their booked listings, including the details of the listing as well as their booked rental period.

![MyBookingsPage](https://user-images.githubusercontent.com/97570310/208283536-f079bc5a-6e1d-4549-9694-916fa93a0b36.png)


### Create Listing
Clicking the "Create Listings" button on the `Home` page, the user is presented with the `Create Listing` page. Here the user can create their own listing by filling out fields such as the title, description, price, and address.

![CreateListingPage](https://user-images.githubusercontent.com/97570310/208283564-d8438f4f-3c7a-4927-ade6-a9e8fd81804c.png)

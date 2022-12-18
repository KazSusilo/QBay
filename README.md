[![Pytest-All](https://github.com/kanchshres/C327-Group-12/actions/workflows/pytest-all.yml/badge.svg?branch=main)](https://github.com/kanchshres/C327-Group-12/actions/workflows/pytest-all.yml)

[![Python PEP8](https://github.com/kanchshres/C327-Group-12/actions/workflows/style_checker.yml/badge.svg?branch=main)](https://github.com/kanchshres/C327-Group-12/actions/workflows/style_checker.yml)

# QBay

An online marketplace for short-term homestay rentals!

## Requirements to Run
Along with Python, these are required to run the program:
```
Flask
Flask-SQLAlchemy
pymysql
```
To install, run `pip install -r requirements.txt` from the root folder
Then, run the program with
```
python3 -m qbay
```
and open the website on `http://127.0.0.1:8081`.

## Running with Docker

Install [docker from their website](https://docs.docker.com/get-docker/). Run the following command from `QBay/docker`:
```
docker-compose up
```
and open the website on `http://0.0.0.0:8081`.



from faker import Faker
from locust import HttpUser, between, task


class MyUser(HttpUser):
    #wait_time = between(1, 2.5)

    host = "https://restful-booker.herokuapp.com"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fake = Faker()

    @task
    def getBooking(self):
        endpoint = "/booking"
        headers = {"Content-Type": "application/json"}
        self.client.get(endpoint, headers=headers)

    @task
    def postBooking(self):
        endpoint = "/booking"
        headers = {"Content-Type": "application/json", "accept": "application/json"}
        payload = {
            "firstname": self.fake.first_name(),
            "lastname": self.fake.last_name(),
            "totalprice": self.fake.random_int(min=100, max=1000),
            "depositpaid": self.fake.boolean(),
            "bookingdates": {
                "checkin": self.fake.date_between(start_date='-30d', end_date='today').strftime('%Y-%m-%d'),
                "checkout": self.fake.date_between(start_date='today', end_date='+30d').strftime('%Y-%m-%d'),
            },
            "additionalneeds": self.fake.random_element(elements=("Breakfast", "Lunch", "Dinner", "WiFi"))
        }

        self.client.post(endpoint, json=payload, headers=headers)

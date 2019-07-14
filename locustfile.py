from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def login(self):
        self.client.post("/studentlogin", {"username": "long", "password": "123"})

    @task(2)
    def index(self):
        self.client.get("/exam", cookies={"username": "long"})

    @task(1)
    def profile(self):
        self.client.get("/")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    host = 'http://192.168.2.118:8080'
    min_wait = 500
    max_wait = 3000

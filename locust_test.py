from locust import HttpUser, task, between
import random

tracking_numbers = [
    'LV611586092CN', 'LV617908564CN', 'LV611585684CN', 'RG008482666CN', 'CY012011836CN', 'LV627660811CN',
    'CY012373804CN', 'LA151249639CN', 'LP582688401CN', 'EV029066604CN', 'LV651582139CN', 'LV663202155CN',
    'LV651582350CN', 'LV660539880CN', 'LV668750216CN', 'LV668550223CN', 'LV669594781CN', 'LV668077772CN',
    'LV668077622CN', 'EB780555102CN', 'LR021365770CN', 'LV673862524CN'
]


class MyUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def track_ems(self):
        self.client.get("/ems/track", params={"tracking_number": random.choice(tracking_numbers), "proxy": 1})

    # @task
    # def global_track_trace(self):
    #     self.client.get("/globaltracktrace/track", params={"tracking_number": "GT1234567890", "proxy": 0, "session": 0})
    #

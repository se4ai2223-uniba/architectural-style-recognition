# Load Testing

Are made to understand what is the load that our app could handle.

        pip install locust

- Define user behavior in Python Code.
- Simulate Milions of simultaneus users.

        from locust import HttpUser, task

        class HelloWorldUser(HttpUser):
        @task
        def hello_world(self):
            self.client.get("/hello")
            self.client.get("/world")

## More detail

- create a locustfile.py
- run locust from terminal
- access locust web interface

        class [NAME](HttpUser):
            wait_time = between(1,5)

            @task
            def [FUNCTION NAME](self)
                self.client.get(...)
                
            @task(importance)
            def ...

            def on_start(self)
                self.client.post(...)
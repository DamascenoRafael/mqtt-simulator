from publisher import Publisher


class Simulator:
    def __init__(self, publishers: list[Publisher]):
        self.publishers = publishers

    def run(self):
        for publisher in self.publishers:
            print(f"Starting: {publisher.topic_url} ...")
            publisher.start()

    def stop(self):
        for publisher in self.publishers:
            print(f"Stopping: {publisher.topic_url} ...")
            publisher.stop()

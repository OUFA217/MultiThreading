import logging
import threading
import time
import random

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(levelname)s: %(message)s')

class TrafficLight:
    def __init__(self):
        self.color = "red"
        self.lock = threading.Lock()

    def change_color(self):
        with self.lock:
            if self.color == "red":
                self.color = "green"
                logging.debug("Traffic light changed to green")
            else:
                self.color = "red"
                logging.debug("Traffic light changed to red")

class Vehicle:
    def __init__(self, id, direction):
        self.id = id
        self.direction = direction
        self.lock = threading.Lock()

    def move(self):
        with self.lock:
            logging.debug("Vehicle %d moving in direction %d", self.id, self.direction)
            # simulate vehicle movement
            time.sleep(random.uniform(0.1, 1.0))

class Intersection:
    def __init__(self):
        self.traffic_lights = [TrafficLight() for _ in range(4)]
        self.vehicles = []
        self.lock = threading.Lock()

    def add_vehicle(self, vehicle):
        with self.lock:
            self.vehicles.append(vehicle)
            logging.debug("Added vehicle %d to intersection", vehicle.id)

    def remove_vehicle(self, vehicle):
        with self.lock:
            self.vehicles.remove(vehicle)
            logging.debug("Removed vehicle %d from intersection", vehicle.id)

    def run(self):
        while True:
            for i, traffic_light in enumerate(self.traffic_lights):
                # change traffic light color
                traffic_light.change_color()

                # allow vehicles to pass through intersection
                with self.lock:
                    for vehicle in self.vehicles:
                        if vehicle.direction == i and traffic_light.color == "green":
                            vehicle.move()

            # simulate time between traffic light changes
            time.sleep(5)
            logging.debug("Simulated time between traffic light changes")

if __name__ == '__main__':
    # create intersection and start simulation
    intersection = Intersection()
    intersection_thread = threading.Thread(target=intersection.run)
    intersection_thread.start()

    # create vehicles and add them to intersection
    for i in range(20):
        vehicle_direction = random.randint(0, 3)
        vehicle = Vehicle(i, vehicle_direction)
        intersection.add_vehicle(vehicle)

    # simulate vehicles leaving intersection
    while True:
        with intersection.lock:
            if not intersection.vehicles:
                break

        # simulate time between vehicle removals
        time.sleep(1)

        # remove random vehicle from intersection
        with intersection.lock:
            vehicle = random.choice(intersection.vehicles)
            intersection.remove_vehicle(vehicle)

    # wait for intersection simulation to finish
    intersection_thread.join()
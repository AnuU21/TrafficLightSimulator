import pygame
import time
import threading
from light_control import *
from vehicle import *
from pedestrian import *
import random

controller = TrafficIntersectionController()
switch_interval = 3

def updateLights():
    while True:
        current_state = controller.get_current_state()
        new_state = current_state % 4 + 1

        time.sleep(switch_interval)
        controller.switch_state(new_state)


pygame.init()

thread2 = threading.Thread(name="updateLights",target=updateLights, args=())
thread2.daemon = True
thread2.start()

# Set up the drawing window
screen = pygame.display.set_mode([800, 800])

background_image = pygame.image.load('images/intersection.png')

# Resize intersection image
background = pygame.transform.scale(background_image, (800,800))

all_vehicles = pygame.sprite.Group()
all_pedestrians = pygame.sprite.Group()

opposite_direction_map = {
        Direction.NORTH: Direction.SOUTH,
        Direction.SOUTH: Direction.NORTH,
        Direction.EAST: Direction.WEST,
        Direction.WEST: Direction.EAST
    }

def spawn_vehicle():
    # Simplified origin and destination selection to prevent same-origin-destination issue
    origin = random.choice(list(Direction))
    destination = random.choice([d for d in Direction if d != origin])
    vehicle = Vehicle(origin, destination)
    all_vehicles.add(vehicle)
    vehicle.turn(opposite_direction_map[origin])

    print(f"Vehicle spawned at {origin} heading to {destination}")

def spawn_pedestrian():
    origin = random.choice(list(PedestrianDirection))
    destination = pedestrian_opposite_direction_map[origin]
    pedestrian = Pedestrian(origin, destination)
    all_pedestrians.add(pedestrian)
    pedestrian.go_straight(pedestrian_opposite_direction_map[origin])

    print(f"Pedestrian spawned at {origin} heading to {destination}")

def pedestrian_has_reached_intersection(pedestrian: Pedestrian):
    if pedestrian.origin == PedestrianDirection.NORTH1 or pedestrian.origin == PedestrianDirection.NORTH2:
        return pedestrian.y == 250 or pedestrian.y == 251
    elif pedestrian.origin == PedestrianDirection.SOUTH1 or pedestrian.origin == PedestrianDirection.SOUTH2:
        return pedestrian.y == 480 or pedestrian.y == 481
    elif pedestrian.origin == PedestrianDirection.WEST1 or pedestrian.origin == PedestrianDirection.WEST2:
        return pedestrian.x == 250 or pedestrian.x == 251
    elif pedestrian.origin == PedestrianDirection.EAST1 or pedestrian.origin == PedestrianDirection.EAST2:
        return pedestrian.x == 480 or pedestrian.x == 481


def move_pedestrians():
    for pedestrian in all_pedestrians:
        traffic_signal = None

        if pedestrian.origin == PedestrianDirection.NORTH1:
            traffic_signal = controller.pd8.get_signal()
        elif pedestrian.origin == PedestrianDirection.SOUTH1:
            traffic_signal = controller.pd1.get_signal()
        elif pedestrian.origin == PedestrianDirection.NORTH2:
            traffic_signal = controller.pd5.get_signal()
        elif pedestrian.origin == PedestrianDirection.SOUTH2:
            traffic_signal = controller.pd4.get_signal()
        elif pedestrian.origin == PedestrianDirection.WEST1:
            traffic_signal = controller.pd3.get_signal()
        elif pedestrian.origin == PedestrianDirection.WEST2:
            traffic_signal = controller.pd6.get_signal()
        elif pedestrian.origin == PedestrianDirection.EAST1:
            traffic_signal = controller.pd2.get_signal()
        elif pedestrian.origin == PedestrianDirection.EAST2:
            traffic_signal = controller.pd7.get_signal()

        if pedestrian_has_reached_intersection(pedestrian) and not pedestrian.has_crossed:
            pedestrian.pedestrian_act_on_traffic_light(traffic_signal)
        else:
            pedestrian.go_straight(pedestrian.direction)


def remove_vehicles(all_vehicles):
    current_time = time.time()
    for vehicle in list(all_vehicles):  # Use list to avoid modifying the group while iterating
        if current_time - vehicle.timestamp > 20:
            all_vehicles.remove(vehicle)
            print(f"Vehicle removed after 20 seconds.")


def has_reached_intersection(vehicle: Vehicle):
    if vehicle.origin == Direction.NORTH:
        return vehicle.y == 200 or vehicle.y == 201
    elif vehicle.origin == Direction.SOUTH:
        return vehicle.y == 575 or vehicle.y == 576
    elif vehicle.origin == Direction.EAST:
        return vehicle.x == 575 or vehicle.x == 576
    elif vehicle.origin == Direction.WEST:
        return vehicle.x == 200 or vehicle.x == 201

    
def find_next_vehicle_in_path(vehicle, all_vehicles):
    safety_distance = 60  # Define a safety distance (in pixels)
    for other_vehicle in all_vehicles:
        if vehicle == other_vehicle:
            continue  # Skip the vehicle itself

        # Check if the other vehicle is in the same direction of movement
        if vehicle.direction == other_vehicle.direction:
            if (vehicle.direction == Direction.NORTH) and (vehicle.y > other_vehicle.y) and ((vehicle.y - other_vehicle.y) < safety_distance):
                return other_vehicle
            elif (vehicle.direction == Direction.SOUTH) and (vehicle.y < other_vehicle.y) and ((other_vehicle.y - vehicle.y) < safety_distance):
                return other_vehicle
            elif (vehicle.direction == Direction.EAST) and (vehicle.x < other_vehicle.x) and ((other_vehicle.x - vehicle.x) < safety_distance):
                return other_vehicle
            elif (vehicle.direction == Direction.WEST) and (vehicle.x > other_vehicle.x) and ((vehicle.x - other_vehicle.x) < safety_distance):
                return other_vehicle
    return None  # If no vehicle is found in the path, return None



def move_vehicles():
    for vehicle in all_vehicles:
        # print(f"Vehicle at {vehicle.x}, {vehicle.y}")
        # Skip if vehicle has reached its destination (this logic might need adjustments)

        # Implement logic to check for red light and stop vehicles accordingly
        traffic_signal = None
        if vehicle.origin == Direction.NORTH:
            traffic_signal = controller.ts1.get_signal()
        elif vehicle.origin == Direction.SOUTH:
            traffic_signal = controller.ts3.get_signal()
        elif vehicle.origin == Direction.EAST:
            traffic_signal = controller.ts2.get_signal()
        elif vehicle.origin == Direction.WEST:
            traffic_signal = controller.ts4.get_signal()

        # Check if vehicle has reached the intersection and act on traffic signal
        if has_reached_intersection(vehicle) and (not vehicle.has_crossed):
            vehicle.act_on_traffic_light(traffic_signal)
            
            
        else:
            # Simplified collision avoidance by checking distance to the next vehicle
            # This is a placeholder for actual collision detection logic
            next_vehicle = find_next_vehicle_in_path(vehicle, all_vehicles)  # Pseudo-function
            if next_vehicle and vehicle.is_close_to(next_vehicle):
                vehicle.stop()
            else:
                vehicle.go_straight(vehicle.direction)


SPAWN_INTERVAL = 4
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, SPAWN_INTERVAL * 1000)
    
# Run until the user asks to quit
running = True


while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == SPAWN_EVENT:
            print("Spawning vehicle")
            spawn_vehicle()
            spawn_pedestrian()
        
    
    move_vehicles()
    move_pedestrians()
    remove_vehicles(all_vehicles)
    
    
    pd3_resize = pygame.transform.scale(controller.pd3.image, (80, 80))
    pd4_resize = pygame.transform.scale(controller.pd4.image, (80, 80))
    pd5_resize = pygame.transform.scale(controller.pd5.image, (80, 80))
    pd6_resize = pygame.transform.scale(controller.pd6.image, (80, 80))
    pd7_resize = pygame.transform.scale(controller.pd7.image, (80, 80))
    pd8_resize = pygame.transform.scale(controller.pd8.image, (80, 80))

    screen.blit(background,(0,0))
    screen.blit(pygame.transform.rotate(controller.ts1.image, 180), (335, 50))
    screen.blit(pygame.transform.rotate(controller.ts2.image, 90), (650, 335))
    screen.blit(controller.ts3.image, (410, 650))
    screen.blit(pygame.transform.rotate(controller.ts4.image, 270), (50, 400))
    
    screen.blit(controller.pd1.image, (210, 250))
    screen.blit(pygame.transform.rotate(controller.pd2.image, 90), (250, 210))
    screen.blit(pygame.transform.rotate(controller.pd3.image, 270), (480, 210))
    screen.blit(controller.pd4.image, (550, 250))
    screen.blit(pygame.transform.rotate(controller.pd5.image, 180), (550, 480))
    screen.blit(pygame.transform.rotate(controller.pd6.image, 270), (480, 550))
    screen.blit(pygame.transform.rotate(controller.pd7.image, 90), (250, 550))
    screen.blit(pygame.transform.rotate(controller.pd8.image, 180), (210, 480))


    for vehicle in all_vehicles:
        screen.blit(vehicle.image, (vehicle.x, vehicle.y))

    for pedestrian in all_pedestrians:
        screen.blit(pedestrian.image, (pedestrian.x, pedestrian.y))

    pygame.display.update()

# Done! Time to quit.
pygame.quit()

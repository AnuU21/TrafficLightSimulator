import pygame
import time
import threading
from light_control import *
from vehicle import *
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
            if vehicle.direction == Direction.NORTH and vehicle.y < other_vehicle.y and other_vehicle.y - vehicle.y < safety_distance:
                return other_vehicle
            elif vehicle.direction == Direction.SOUTH and vehicle.y > other_vehicle.y and vehicle.y - other_vehicle.y < safety_distance:
                return other_vehicle
            elif vehicle.direction == Direction.EAST and vehicle.x < other_vehicle.x and other_vehicle.x - vehicle.x < safety_distance:
                return other_vehicle
            elif vehicle.direction == Direction.WEST and vehicle.x > other_vehicle.x and vehicle.x - other_vehicle.x < safety_distance:
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
        
    
    move_vehicles()
    remove_vehicles(all_vehicles)
    
    
    

    screen.blit(background,(0,0))
    screen.blit(pygame.transform.rotate(controller.ts1.image, 180), (335, 50))
    screen.blit(pygame.transform.rotate(controller.ts2.image, 90), (650, 335))
    screen.blit(controller.ts3.image, (410, 650))
    screen.blit(pygame.transform.rotate(controller.ts4.image, 270), (50, 400))

    for vehicle in all_vehicles:
        screen.blit(vehicle.image, (vehicle.x, vehicle.y))

    pygame.display.update()

# Done! Time to quit.
pygame.quit()


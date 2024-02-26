import pygame
from enum import Enum
from light_control import SignalColor
import time

class PedestrianDirection(Enum):
    SOUTH1 = {"x": 250, "y": 750}
    SOUTH2 = {"x": 480, "y": 750}
    EAST1 = {"x": 750, "y": 250}
    EAST2 = {"x": 750, "y": 480}
    NORTH1 = {"x": 250, "y": 0}
    NORTH2 = {"x": 480, "y": 0}
    WEST1 = {"x": 0, "y": 250}
    WEST2 = {"x": 0, "y": 480}

pedestrian_opposite_direction_map = {
        PedestrianDirection.NORTH1: PedestrianDirection.SOUTH1,
        PedestrianDirection.SOUTH1: PedestrianDirection.NORTH1,
        PedestrianDirection.EAST1: PedestrianDirection.WEST1,
        PedestrianDirection.WEST1: PedestrianDirection.EAST1,
        PedestrianDirection.NORTH2: PedestrianDirection.SOUTH2,
        PedestrianDirection.SOUTH2: PedestrianDirection.NORTH2,
        PedestrianDirection.EAST2: PedestrianDirection.WEST2,
        PedestrianDirection.WEST2: PedestrianDirection.EAST2
    }


class Pedestrian(pygame.sprite.Sprite):
    def __init__(self, origin: PedestrianDirection, destination: PedestrianDirection):
        pygame.sprite.Sprite.__init__(self)
        self.timestamp = time.time()
        
        self.origin = origin
        self.destination = destination
        self.direction = pedestrian_opposite_direction_map[origin]
        self.has_crossed = False
        self.reached_intersection = False
        


        self.image = pygame.image.load("images/pedestrian.png")

        
        self.rect = self.image.get_rect()
        self.original_image = self.image
        
        
        self.x = origin.value["x"]
        self.y = origin.value["y"]

    
    def go_straight(self, direction: PedestrianDirection):
        if direction == PedestrianDirection.NORTH1:
            self.y -= 1
        elif direction == PedestrianDirection.SOUTH1:
            self.y += 1
        elif direction == PedestrianDirection.EAST1:
            self.x += 1
        elif direction == PedestrianDirection.WEST1:
            self.x -= 1
        elif direction == PedestrianDirection.NORTH2:
            self.y -= 1
        elif direction == PedestrianDirection.SOUTH2:
            self.y += 1
        elif direction == PedestrianDirection.EAST2:
            self.x += 1
        elif direction == PedestrianDirection.WEST2:
            self.x -= 1
        
    
    def pedestrian_reach_intersection(self):
        target_x, target_y = self.get_intersection_target()
        self.x, self.y = target_x, target_y
        self.has_crossed = True
        print("Pedestrian has reached and is crossing the intersection.")
    

    # Get the intersection target position based on the destination
    def get_intersection_target(self):
        return {
            PedestrianDirection.SOUTH1: (250, 425),
            PedestrianDirection.NORTH1: (425, 250),
            PedestrianDirection.WEST1: (425, 250),
            PedestrianDirection.EAST1: (250, 425),
            PedestrianDirection.SOUTH2: (480, 425),
            PedestrianDirection.NORTH2: (425, 480),
            PedestrianDirection.WEST2: (425, 480),
            PedestrianDirection.EAST2: (480, 425)
        }.get(self.destination, (0, 0))


    # Simplify and consolidate logic in act_on_traffic_light method
    def pedestrian_act_on_traffic_light(self, traffic_light_color: SignalColor):
        action_map = self.get_action_map()
        print(self.origin, self.destination, traffic_light_color)
        action = action_map.get((self.origin, self.destination, traffic_light_color))

        if action:
            action()  # Call the action function

    def get_action_map(self):
        return {
            (PedestrianDirection.SOUTH1, PedestrianDirection.NORTH1, SignalColor.PDGREEN): lambda: self.go_straight(PedestrianDirection.NORTH1),
            (PedestrianDirection.SOUTH2, PedestrianDirection.NORTH2, SignalColor.PDGREEN): lambda: self.go_straight(PedestrianDirection.NORTH2),
            (PedestrianDirection.EAST1, PedestrianDirection.WEST1, SignalColor.PDGREEN): lambda: self.go_straight(PedestrianDirection.WEST1),
            (PedestrianDirection.EAST2, PedestrianDirection.WEST2, SignalColor.PDGREEN): lambda: self.go_straight(PedestrianDirection.WEST2),
            (PedestrianDirection.WEST1, PedestrianDirection.EAST1, SignalColor.PDGREEN): lambda: self.go_straight(PedestrianDirection.EAST1),
            (PedestrianDirection.WEST2, PedestrianDirection.EAST2, SignalColor.PDGREEN): lambda: self.go_straight(PedestrianDirection.EAST2),
            (PedestrianDirection.NORTH1, PedestrianDirection.SOUTH1, SignalColor.PDGREEN): lambda: self.go_straight(PedestrianDirection.SOUTH1),
            (PedestrianDirection.NORTH2, PedestrianDirection.SOUTH2, SignalColor.PDGREEN): lambda: self.go_straight(PedestrianDirection.SOUTH2),
        }

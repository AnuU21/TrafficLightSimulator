import pygame
from enum import Enum
from light_control import SignalColor
import time

class Direction(Enum):
    SOUTH1 = {"x": 250, "y": 750}
    SOUTH2 = {"x": 480, "y": 750}
    EAST1 = {"x": 750, "y": 250}
    EAST2 = {"x": 750, "y": 480}
    NORTH1 = {"x": 250, "y": 0}
    NORTH2 = {"x": 480, "y": 0}
    WEST1 = {"x": 0, "y": 250}
    WEST2 = {"x": 0, "y": 480}

opposite_direction_map = {
        Direction.NORTH1: Direction.SOUTH1,
        Direction.SOUTH1: Direction.NORTH1,
        Direction.EAST1: Direction.WEST1,
        Direction.WEST1: Direction.EAST1,
        Direction.NORTH2: Direction.SOUTH2,
        Direction.SOUTH2: Direction.NORTH2,
        Direction.EAST2: Direction.WEST2,
        Direction.WEST2: Direction.EAST2
    }


class Pedestrian(pygame.sprite.Sprite):
    def __init__(self, origin: Direction, destination: Direction):
        pygame.sprite.Sprite.__init__(self)
        self.timestamp = time.time()
        
        self.origin = origin
        self.destination = destination
        self.direction = opposite_direction_map[origin]
        self.has_crossed = False
        self.reached_intersection = False
        
        self.image = pygame.image.load("images/pedestrian.png")
        
        self.rect = self.image.get_rect()
        self.original_image = self.image
        
        self.x = origin.value["x"]
        self.y = origin.value["y"]


    def stop(self):
        self.x = self.x
        self.y = self.y
    
    def go_straight(self, direction: Direction):
        if direction == Direction.NORTH1:
            self.y -= .2
        elif direction == Direction.SOUTH1:
            self.y += .2
        elif direction == Direction.EAST1:
            self.x += .2
        elif direction == Direction.WEST1:
            self.x -= .2
        elif direction == Direction.NORTH2:
            self.y -= .2
        elif direction == Direction.SOUTH2:
            self.y += .2
        elif direction == Direction.EAST2:
            self.x += .2
        elif direction == Direction.WEST2:
            self.x -= .2
        
    
    def reach_intersection(self):
        target_x, target_y = self.get_intersection_target()
        self.x, self.y = target_x, target_y
        self.has_crossed = True
        print("Pedestrian has reached and is crossing the intersection.")
    

    # Get the intersection target position based on the destination
    def get_intersection_target(self):
        return {
            Direction.SOUTH1: (250, 425),
            Direction.NORTH1: (425, 250),
            Direction.WEST1: (425, 250),
            Direction.EAST1: (250, 425),
            Direction.SOUTH2: (480, 425),
            Direction.NORTH2: (425, 480),
            Direction.WEST2: (425, 480),
            Direction.EAST2: (480, 425)
        }.get(self.destination, (0, 0))


    # Simplify and consolidate logic in act_on_traffic_light method
    def act_on_traffic_light(self, traffic_light_color: SignalColor):
        action_map = self.get_action_map()
        action = action_map.get((self.origin, self.destination, traffic_light_color))
        
        if action:
            action()  # Call the action function
        else:
            self.stop()

    def get_action_map(self):
        return {
            (Direction.SOUTH1, Direction.NORTH1, SignalColor.PDGREEN): lambda: self.go_straight(Direction.NORTH1),
            (Direction.SOUTH2, Direction.NORTH2, SignalColor.PDGREEN): lambda: self.go_straight(Direction.NORTH2),
            (Direction.EAST1, Direction.WEST1, SignalColor.PDGREEN): lambda: self.go_straight(Direction.WEST1),
            (Direction.EAST2, Direction.WEST2, SignalColor.PDGREEN): lambda: self.go_straight(Direction.WEST2),
            (Direction.WEST1, Direction.EAST1, SignalColor.PDGREEN): lambda: self.go_straight(Direction.EAST1),
            (Direction.WEST2, Direction.EAST2, SignalColor.PDGREEN): lambda: self.go_straight(Direction.EAST2),
            (Direction.NORTH1, Direction.SOUTH1, SignalColor.PDGREEN): lambda: self.go_straight(Direction.SOUTH1),
            (Direction.NORTH2, Direction.SOUTH2, SignalColor.PDGREEN): lambda: self.go_straight(Direction.SOUTH2),
        }
    
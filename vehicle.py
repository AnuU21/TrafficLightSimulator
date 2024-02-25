import pygame
from enum import Enum
from light_control import SignalColor
import time

class Direction(Enum):
	SOUTH = {"x": 425, "y": 750}
	EAST = {"x": 750, "y": 350}
	NORTH = {"x": 350, "y": 0}
	WEST = {"x": 0, "y": 425}

opposite_direction_map = {
        Direction.NORTH: Direction.SOUTH,
        Direction.SOUTH: Direction.NORTH,
        Direction.EAST: Direction.WEST,
        Direction.WEST: Direction.EAST
    }


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, origin: Direction, destination: Direction):
        pygame.sprite.Sprite.__init__(self)
        self.timestamp = time.time()
        
        self.origin = origin
        self.destination = destination
        self.direction = opposite_direction_map[origin]
        self.has_crossed = False
        self.reached_intersection = False
        


        self.image = pygame.image.load("images/car.png")

        
        self.rect = self.image.get_rect()
        self.original_image = self.image
        
        
        self.x = origin.value["x"]
        self.y = origin.value["y"]


    def stop(self):
        self.x = self.x
        self.y = self.y
    
    def go_straight(self, direction: Direction):
        if direction == Direction.NORTH:
            self.y -= 2
        elif direction == Direction.SOUTH:
            self.y += 2
        elif direction == Direction.EAST:
            self.x += 2
        elif direction == Direction.WEST:
            self.x -= 2
        
    def turn(self, direction: Direction):
        if direction == Direction.NORTH:
            self.image = pygame.transform.rotate(self.original_image, 0)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.go_straight(direction)
        elif direction == Direction.SOUTH:

            self.image = pygame.transform.rotate(self.original_image, 180)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.go_straight(direction)
        elif direction == Direction.EAST:
         
            self.image = pygame.transform.rotate(self.original_image, 270)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.go_straight(direction)
        elif direction == Direction.WEST:
         
            self.image = pygame.transform.rotate(self.original_image, 90)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.go_straight(direction)
        

        self.rect = self.image.get_rect(center=self.rect.center)
        self.direction = direction
    
    def is_close_to(self, next_vehicle):
        # Define safety distances for horizontal and vertical lanes
        horizontal_safety_distance = 60
        vertical_safety_distance = 85

        # Check if both vehicles are in the same lane and direction
        if self.direction == next_vehicle.direction:
            dx = abs(next_vehicle.x - self.x)
            dy = abs(self.y - next_vehicle.y)
            if self.direction == Direction.WEST or self.direction == Direction.EAST:
                distance = dx
                return distance < horizontal_safety_distance
            else:
                distance = dy
                print(distance)
                return distance < vertical_safety_distance
        return False
    
    def reach_intersection(self):
        target_x, target_y = self.get_intersection_target()
        self.x, self.y = target_x, target_y
        self.has_crossed = True
        print("Vehicle has reached and is crossing the intersection.")

    # Get the intersection target position based on the destination
    def get_intersection_target(self):
        return {
            Direction.SOUTH: (350, 425),
            Direction.NORTH: (425, 350),
            Direction.WEST: (425, 350),
            Direction.EAST: (350, 425)
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
            (Direction.SOUTH, Direction.NORTH, SignalColor.STRAIGHT): lambda: self.go_straight(Direction.NORTH),
            (Direction.SOUTH, Direction.WEST, SignalColor.LEFT): lambda: self.move_and_reach(Direction.WEST),
            (Direction.SOUTH, Direction.EAST, SignalColor.RIGHT): lambda: self.move_and_reach(Direction.EAST),
            (Direction.EAST, Direction.WEST, SignalColor.STRAIGHT): lambda: self.go_straight(Direction.WEST),
            (Direction.EAST, Direction.SOUTH, SignalColor.LEFT): lambda: self.move_and_reach(Direction.SOUTH),
            (Direction.EAST, Direction.NORTH, SignalColor.RIGHT): lambda: self.move_and_reach(Direction.NORTH),
            (Direction.NORTH, Direction.SOUTH, SignalColor.STRAIGHT): lambda: self.go_straight(Direction.SOUTH),
            (Direction.NORTH, Direction.EAST, SignalColor.LEFT): lambda: self.move_and_reach(Direction.EAST),
            (Direction.NORTH, Direction.WEST, SignalColor.RIGHT): lambda: self.move_and_reach(Direction.WEST),
            (Direction.WEST, Direction.EAST, SignalColor.STRAIGHT): lambda: self.go_straight(Direction.EAST),
            (Direction.WEST, Direction.NORTH, SignalColor.RIGHT): lambda: self.move_and_reach(Direction.NORTH),
            (Direction.WEST, Direction.SOUTH, SignalColor.LEFT): lambda: self.move_and_reach(Direction.SOUTH),
        }
    
    
    def move_and_reach(self, direction):
        self.move_in_direction(direction)
        if not self.has_crossed:
            self.reach_intersection()
        self.turn(direction)

    def move_in_direction(self, direction):
        move_map = {
            Direction.NORTH: lambda: setattr(self, 'y', self.y - 2),
            Direction.SOUTH: lambda: setattr(self, 'y', self.y + 2),
            Direction.EAST: lambda: setattr(self, 'x', self.x + 2),
            Direction.WEST: lambda: setattr(self, 'x', self.x - 2),
        }
        move_map.get(direction, lambda: None)()

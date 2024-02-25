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


        self.image = pygame.image.load("images/up/car.png")

        
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
        
    def turn(self, destination: Direction):
        if destination == Direction.NORTH:
            self.image = pygame.transform.rotate(self.original_image, 0)
            self.go_straight(destination)
        elif destination == Direction.SOUTH:

            self.image = pygame.transform.rotate(self.original_image, 180)
            self.go_straight(destination)
        elif destination == Direction.EAST:
         
            self.image = pygame.transform.rotate(self.original_image, 270)
            self.go_straight(destination)
        elif destination == Direction.WEST:
         
            self.image = pygame.transform.rotate(self.original_image, 90)
            self.go_straight(destination)
        

        self.rect = self.image.get_rect(center=self.rect.center)
        self.direction = destination
    
    def is_close_to(self, next_vehicle):
    # Check if both vehicles are in the same lane and direction
        if self.direction == next_vehicle.direction:
            dx = abs(next_vehicle.x - self.x)
            dy = abs(next_vehicle.y - self.y)
            if self.direction == Direction.NORTH or self.direction == Direction.SOUTH:
                distance = dy
            else:
                distance = dx
            # Consider vehicles close if they are less than 10 pixels apart
            # print(distance)
            return distance < 60
        return False
    
    def reach_intersection(self):
        target_x, target_y = 0, 0
        if self.destination == Direction.SOUTH:
            target_x = 350
            target_y = 425
        elif self.destination == Direction.NORTH:
            target_x = 425
            target_y = 350
        elif self.destination == Direction.WEST:
            target_y = 350
            target_x = 425
        elif self.destination == Direction.EAST:
            target_y = 425
            target_x = 350
            
        # Ensure has_crossed flag is correctly checked
        self.x += (2 if self.x < target_x else -2)
        self.y += (2 if self.y < target_y else -2)
        self.has_crossed = True
        if self.has_crossed:
            print("Attempting to move towards intersection...")

            # Adjust movement logic to ensure it's triggered correctly
            
            print("Vehicle is moving towards the intersection.")

            # Calculate the distance to the intersection
            dist_x = abs(self.x - target_x)
            dist_y = abs(self.y - target_y)

            for i in range(0, dist_x):
                self.x += (2 if self.x < target_x else -2)
                if abs(self.x - target_x) < 2:
                    self.x = target_x
            
            for i in range(0, dist_y):
                self.y += (2 if self.y < target_y else -2)
                if abs(self.y - target_y) < 2:
                    self.y = target_y
        
                

            # Update reached_intersection flag based on actual position
            self.reached_intersection = (self.x == target_x and self.y == target_y)
            if self.reached_intersection:
                self.has_crossed = True
                print("Vehicle has reached and is crossing the intersection.")


    def act_on_traffic_light(self, traffic_light_color: SignalColor):
        if self.origin == Direction.SOUTH:
            if self.destination == Direction.NORTH and traffic_light_color == SignalColor.STRAIGHT:
                self.y -= 2
                if not self.has_crossed:
                    self.reach_intersection()

                self.go_straight(self.direction)
            elif self.destination == Direction.WEST and traffic_light_color == SignalColor.LEFT:
                self.y -= 2
                if not self.has_crossed:
                    self.reach_intersection()
                
                self.turn(Direction.WEST)
            elif self.destination == Direction.EAST and traffic_light_color == SignalColor.RIGHT:
                self.y -= 2
                if not self.has_crossed:
                    self.reach_intersection()
                self.turn(Direction.EAST)
            else:
                self.stop()
        elif self.origin == Direction.NORTH:
            if self.destination == Direction.SOUTH and traffic_light_color == SignalColor.STRAIGHT:
                self.y += 2
                if not self.has_crossed:
                    self.reach_intersection()
                self.go_straight(self.direction)
            elif self.destination == Direction.WEST and traffic_light_color == SignalColor.RIGHT:
                self.y += 2
                if not self.has_crossed:
                    self.reach_intersection()
                self.turn(Direction.WEST)
            elif self.destination == Direction.EAST and traffic_light_color == SignalColor.LEFT:
                self.y += 2
                if not self.has_crossed:
                    self.reach_intersection()
                self.turn(Direction.EAST)
            else:
                self.stop()
        elif self.origin == Direction.WEST:
            if self.destination == Direction.EAST and traffic_light_color == SignalColor.STRAIGHT:
                self.x += 2
                self.reach_intersection()
                self.go_straight(self.direction)
            elif self.destination == Direction.SOUTH and traffic_light_color == SignalColor.RIGHT:
                self.x += 2
                self.reach_intersection()
                self.turn(Direction.SOUTH)
            elif self.destination == Direction.NORTH and traffic_light_color == SignalColor.LEFT:
                self.x += 2
                self.reach_intersection()
                self.turn(Direction.NORTH)
            else:
                self.stop()
        elif self.origin == Direction.EAST:
            if self.destination == Direction.WEST and traffic_light_color == SignalColor.STRAIGHT:
                self.x -= 2
                self.reach_intersection()
                self.go_straight(self.direction)
            elif self.destination == Direction.SOUTH and traffic_light_color == SignalColor.LEFT:
                self.x -= 2
                self.reach_intersection()
                self.turn(Direction.SOUTH)
            elif self.destination == Direction.NORTH and traffic_light_color == SignalColor.RIGHT:
                self.x -= 2
                self.reach_intersection()
                self.turn(Direction.NORTH)
            else:
                self.stop()

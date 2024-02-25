import pygame
from enum import Enum
from light_control import SignalColor

class Direction(Enum):
	NORTH = {"x": 400, "y": 800}
	EAST = {"x": 800, "y": 400}
	SOUTH = {"x": 400, "y": 0}
	WEST = {"x": 0, "y": 400}


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, origin: Direction, destination: Direction):
        pygame.sprite.Sprite.__init__(self)
        
        self.origin = origin
        self.image = pygame.image.load("images/up/car.png")
        self.rect = self.image.get_rect()
        self.destination = destination
        
        self.x = origin.value["x"]
        self.y = origin.value["y"]


    def stop(self):
        # Logic here
        pass
    
    def go_straight(self, direction: Direction):
        if direction == Direction.NORTH:
            self.y -= 1
        elif direction == Direction.SOUTH:
            self.y += 1
        elif direction == Direction.EAST:
            self.x += 1
        elif direction == Direction.WEST:
            self.x -= 1
        
    def turn(self, destination: Direction):
        if destination == Direction.NORTH:
            self.image = pygame.transform.rotate(self.image, 0)
        elif destination == Direction.SOUTH:
            self.image = pygame.transform.rotate(self.image, 180)
        elif destination == Direction.EAST:
            self.image = pygame.transform.rotate(self.image, 270)
        elif destination == Direction.WEST:
            self.image = pygame.transform.rotate(self.image, 90)
        

        self.rect = self.image.get_rect(center=self.rect.center)
        self.direction = destination

    def act_on_traffic_light(self, traffic_light_color: SignalColor):
        if self.origin == Direction.SOUTH:
            if self.destination == Direction.NORTH and traffic_light_color == SignalColor.STRAIGHT:
                self.go_straight()
            elif self.destination == Direction.WEST and traffic_light_color == SignalColor.LEFT:
                self.turn(self, Direction.WEST)
            elif self.destination == Direction.EAST and traffic_light_color == SignalColor.RIGHT:
                self.turn(self, Direction.EAST)
            else:
                self.stop()
        elif self.origin == Direction.NORTH:
            if self.destination == Direction.SOUTH and traffic_light_color == SignalColor.STRAIGHT:
                self.go_straight()
            elif self.destination == Direction.WEST and traffic_light_color == SignalColor.RIGHT:
                self.turn(self, Direction.WEST)
            elif self.destination == Direction.EAST and traffic_light_color == SignalColor.LEFT:
                self.turn(self, Direction.EAST)
            else:
                self.stop()
        elif self.origin == Direction.WEST:
            if self.destination == Direction.EAST and traffic_light_color == SignalColor.STRAIGHT:
                self.go_straight()
            elif self.destination == Direction.SOUTH and traffic_light_color == SignalColor.RIGHT:
                self.turn(self, Direction.SOUTH)
            elif self.destination == Direction.NORTH and traffic_light_color == SignalColor.LEFT:
                self.turn(self, Direction.NORTH)
            else:
                self.stop()
        elif self.origin == Direction.EAST:
            if self.destination == Direction.WEST and traffic_light_color == SignalColor.STRAIGHT:
                self.go_straight()
            elif self.destination == Direction.SOUTH and traffic_light_color == SignalColor.LEFT:
                self.turn(self, Direction.SOUTH)
            elif self.destination == Direction.NORTH and traffic_light_color == SignalColor.RIGHT:
                self.turn(self, Direction.NORTH)
            else:
                self.stop()

    
       
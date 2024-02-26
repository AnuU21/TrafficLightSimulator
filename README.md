Car image from https://github.com/mihir-m-gandhi/Adaptive-Traffic-Signal-Timer

Please run:
```
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

light_control.py controls the state of the lights
We have 4 total states for the vehicle traffic lights - straight for north and south, straight for east and west, left for vehicles moving vertically upwards and right for
vehicles moving horizontally right, left for vehicles moving vertically downwards and right for vehicles moving horizontally left

vehicle.py controls the movement of vehicles and their states
vehicles stop at red lights and at green lights when their desired turn is not green
vehicles rotate left or right for turns

pedestrian.py controls the movement of pedestrians and their states
pedestrians stop at red pedestrian lights and go at green pedestrian lights

game.py creates movements and runs the game
pedestrians and vehicles move and stop corresponding to signals


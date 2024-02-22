## Lab 1, Part B
### Advanced Mapping and Routing with A* (Steps 6 and 8)
Advanced mapping is implemented in the file advanced_mapping.py, and 
A* search algorithm in path_finder.py In order to test the functions,
run routing_test.py. This generates a grid with obstacles detected along
with the best path across the obstacles.

### Object Detection (Step 7)
Run the file detect.py to get real time object detection. The inferences
print out onto the console.

### Vehicle Driving
In order for the car to follow to an acceptable level of precision the path
generated by A*, we implement some functions for control in vehicle_control.py.

The drive function uses the speed reading from the photo interruptor
to calculate distance traveled. The function stops the car when the distance is reached.

The turn function takes an angle and attempts to make a tank turn to that angle.
Note that it is inaccurate due to grip loss causing hops. The target angle is scaled up 40%
to account for grip loss. The formula used to calculate angle is 

angular velocity * time = w * t = v/r * t

where r is the radius from the center of the car to the point of contact of the wheels with the ground,
approximated as half the distance between the wheels. We then get:

angle = 2/L * v * t

To get degrees, convert from radians:

180/pi * 2/L * v * t

----------------------------------------------
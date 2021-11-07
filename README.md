# First Reasearch Track 1 Assignment
This folder contains

## How to run
The effect of the script running can be seen in a simulator, named Python Robotic Simulator. This is a simple and portable robot simulator developed by [Student Robotics](https://studentrobotics.org).

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Once the dependencies are installed, simply run the `test.py` script to test out the simulator.

The script can be run in the simulator, using `run.py` and passing it the file name, as follows:

```bash
$ python run.py assignment1.py
```
### About the Simulator: Robot API

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].


**Motors**

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```


**Grabber**

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.


**Vision**

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

[sr-api]: https://studentrobotics.org/docs/programming/sr/

**Heading**

The sr.robot library contains support for using a simulated compass unit on the robot. This allows robots to determine the direction it’s facing in the arena.
```python
  from sr.robot import *
  R = Robot()
  heading = R.compass.get_heading()
```
When called, the get_heading method will return the heading of the robot in radians as a float. The heading is in the range 0 to tau (2π), where 0 is the robot facing directly North, and values increasing clockwise.

## Idea - Robot behaviour
The bottom idea to guide the robot along the path was implementing 
![Robot_RT1](https://user-images.githubusercontent.com/91536387/140644164-46320949-0a9e-4663-b170-e6bc68a35287.png)

## Implementation - Code description
The code is structured in a main function and 5 additional functions

### Functions
Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### Main

## System Limitations and Possible Improvements


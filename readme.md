# SkullCam

This is some hacky but working code that uses OpenCV to locate faces,
and then instruct an Arduino which direction to move a pair of pan-tilt servos.

The Python code finds the faces and outputs a direction (up, down, left, right) 
via serial to the Arduino.

The Arduino sketch will instruct the servos to pan back and forth until 
instructed otherwise by the Python code. Given serial input of U, D, L or R, the 
Arduino will move the servos accordingly.

For more information, check out the [project page here](http://exceedindustries.net/projects/skulltrack).
___
<p align="center">
  <img src="docs/photos/CREO_right_2.JPG" />
</p>

# Hawkeye

Autonomous Inspection Robot

## Home Page Content

## Remote Control Functionality Test - Alex Yu 1 MAR 2021

[![Remote Control Functionality Test ](https://github.com/MESMerizing-Engineers/MESMerizing-Engineers/blob/gh-pages/docs/photos/youtube_remote.jpg)](https://youtu.be/hM1WgEU2hRA "Remote Control Functionality Test")



## LCD Display for strain gauge readings - Liam Moore 26 FEB 2021
To comply with ANSI safety standards, this will help monitor the status of the battery.
and will be mounted on the side of the robot
LCD can cycle between different screens
- Display 
  - strain readings
  - battery percentage
  - time of operation
  - operation status
  - faults
  - storage

<p align="center">
  <img src="docs/photos/lcd_display_straingauge.jpg" width= "400" height ="400"/>
</p>

## Redesigned component configuration - Uyen, Nick, Liam 19 FEB 2021
<p align="center">
  <img src="docs/photos/chassis_redesign.JPG" />
</p>

Update from previous week, the inner workings have been moved to improve...



## Turret is ready to be added on to the chassis - Jen Dacanay 3 JAN 2021
<p align="center">
  <img src="docs/photos/turret_built.png" width= "400" height ="400"/>
</p>

Verified the turret was configured corrrectly
  Video shows the turret running the PXTurretTest
  video: https://drive.google.com/file/d/117dKVGQloSPyNrAAyHhqdyB4uHXf9qXf/view?usp=sharing


## We have Mapping! - Alex Yu 24 DEC 2020
With the holidays just around the corner, we are all enjoying some much needed R&R. That said, it's never a bad time to post an update!
<p align="center">
  <img src="docs/photos/Occupancy Map of My House.png" />
</p>

The team started the ROS tutorials just before end of the quarter. Combined with the arrival of the Intel Realsense cameras, I begun work on implementing a SLAM Algorithm. RTABMap has a ready-to-go ROS package that works with just the single D435i depth camera to get us started. Running the RTABMap, we feed the combined depth and color image as well as the camera's oboard imu sensor information. The figure above is a 2-d snapshot of the occupancy map that was generated when I briefly walked around my home. The black areas are believed to be occupied will the white area is open. <br>
<br>For a first time run, I call this a win!. We can definitely see some issues with this though. For example, the black spotting in the living room seems to be an issue. I suspect this is due to the height that I was holding the camera at when walking around the living room. <br> <br> 
Alot more testing is required, but this has been quite the learning experience!<br>
Happy Holidays! - Alex Yu

<div align="center"><H2>HawkEye</H2>
<p align="center">
  <img src="docs/photos/CREO_right.jpg" />
</p>
<H2>Chassis Blowup View</H2>
<p align="center">
  <img src="docs/photos/CREO_chassisblowup.png" />
</p>
<H2>Top View</H2>
<p align="center">
  <img src="docs/photos/CREO_top.jpg" />
</p>
</div>

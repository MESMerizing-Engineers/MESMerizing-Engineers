___

# Hawkeye

Inspection Robot

## Home Page Content

## Turret is ready to be added on to the chassis.



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

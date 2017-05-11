# ParkingLotTracker
This project in conjunction with a web camera tracks how many free spots there is on the parking lot. This project should be able to run on a Raspberry Pi or a similar product.

# To-Do
## Image quality and recognition
- [x] Add background subtraction to remove static objects
- [x] Use Haar-cascading to detect cars using someone elses haar cascades
- [ ] Include basic transformations for further improvement of background subtraction
- [ ] Correctly identify and mark contours of moving objects

Currently, haar-cascades are performing very poorly. If this continues the points below should be addressed.
It should also be noted that haar-cascading might not be necessary. If we were to determine what an object is simply by its size and shape by looking at its contours we could circumvent haar cascades altogether. This does however pose problems when the recognition is not good enough or when things in a size between a person and a car (bike, motorcycle) are introduced into the picture. Food for thought.
## Option 1: Extended Haar-cascading
- [ ] Use Haar-cascading to detect cars using our own haar cascades created with someone elses dataset
- [ ] Use Haar-cascading to detect cars using our own haar cascades created with our own recorded dataset
## Option 2: Identifying the correct objects using contouring
- [ ] Define the look and shape of the contours of a car using (Minimum size, hard edges and line length etc)
- [ ] Clean up contours with appropriate treshold values for our video stream
## Manipulating recognized cars
- [ ] Grant ID to recognized object
- [ ] Be able to recognize the same object in a different frame
- [ ] Draw a vector in the direction the object is heading
- [ ] Draw a line in which if an object passes through, triggers a function that checks and reports vector direction
- [ ] POST result to our database

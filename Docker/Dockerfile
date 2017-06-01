FROM resin/rpi-raspbian:latest

ENV OPENCV_VERSION 3.2.0

# install opencv3 as detailied in: http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/

# update apt
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils

# install necessary build tools
RUN apt-get -qy install build-essential cmake pkg-config unzip wget

# install necessary libraries
RUN apt-get -qy install \
	libjpeg-dev \
	libtiff5-dev \
	libjasper-dev \
	libpng12-dev \
	libavcodec-dev \
	libavformat-dev \
	libswscale-dev \
	libv4l-dev \
	libxvidcore-dev \
	libx264-dev \
	libgtk2.0-dev \
	libatlas-base-dev \
	gfortran \
	python2.7-dev \
	python-pip \
	python-numpy

# download latest source & contrib
RUN cd /tmp && \
	wget -O opencv.zip https://github.com/opencv/opencv/archive/$OPENCV_VERSION.zip && \
	unzip opencv.zip
	
RUN cd /tmp && \
	wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/$OPENCV_VERSION.zip && \
	unzip opencv_contrib.zip

# build opencv
RUN cd /tmp/opencv-$OPENCV_VERSION && \
	mkdir build && \
	cd build && \
	cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D INSTALL_C_EXAMPLES=ON \
	-D BUILD_PYTHON_SUPPORT=ON \
	-D BUILD_NEW_PYTHON_SUPPORT=ON \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D OPENCV_EXTRA_MODULES_PATH=/tmp/opencv_contrib-$OPENCV_VERSION/modules \
	-D BUILD_EXAMPLES=ON .. && \
	make -j4 && \
	make && \
	make install && \
	# ldconfig && \
	make clean
	
# cleanup source
RUN cd /tmp && rm -rf opencv-$OPENCV_VERSION

RUN git clone --branch develop https://github.com/Archheretic/ParkingLotTracker/ 

CMD ["python" "CarTrackerVideo.py"]
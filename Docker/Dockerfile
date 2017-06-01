FROM resin/rpi-raspbian:latest

#Build instructions from pyimagesearch: http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/

# Update package lists in prep for downloading build tools and libraries
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils

# Install all build tools needed
RUN apt-get -qy install build-essential cmake pkg-config unzip wget

# Install all libraries needed
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

# Download source for OpenCV 3.2.0
RUN cd /tmp && \
	wget -O opencv.zip https://github.com/opencv/opencv/archive/3.2.0.zip && \
	unzip opencv.zip
# Download source for OpenCV 3.2.0 contribs
RUN cd /tmp && \
	wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/3.2.0.zip && \
	unzip opencv_contrib.zip

# Builds OpenCV3.2.0 with contribs
RUN cd /tmp/opencv-3.2.0 && \
	mkdir build && \
	cd build && \
	cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D BUILD_NEW_PYTHON_SUPPORT=ON \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D OPENCV_EXTRA_MODULES_PATH=/tmp/opencv_contrib-3.2.0/modules \
	-D BUILD_EXAMPLES=ON .. && \
	make -j4 && \
	make && \
	make install && \
	# ldconfig && \
	make clean
	
# Delete source code after build is complete
RUN cd /tmp && rm -rf opencv-3.2.0

# CMD ["/bin/bash"]
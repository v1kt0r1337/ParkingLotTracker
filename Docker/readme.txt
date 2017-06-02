docker build -t rpi-jessie-opencv3.2-test .

To display windows created by Open CV properly start docker with the following command:

docker run -ti -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
    rickryan/rpi-jessie-opencv3.2-test

To mount a host directory for development (e.g., where source files for your Open CV application are stored) use the -v option for the run command:

docker run -ti -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
    -v hostDirectoryPath:containerDirectory \
    rickryan/rpi-jessie-opencv3.2-test

obviously replacing hostDirectoryPath and containerDirectory

One trick is to move to the directory containing your source code and start the docker container with:

docker run -ti -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
    -v `pwd`:`pwd` -w `pwd` \
    rickryan/rpi-jessie-opencv3.2-test

this will mount your current directory on the host in the same path with the docker container and start you in that directory.
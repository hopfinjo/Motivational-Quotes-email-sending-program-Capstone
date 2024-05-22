# Run application in Container:

- Install Docker on your machine: https://docs.docker.com/desktop/install/windows-install/
- Install Ximg on your machine: (Ximg is needed to display GUI from application)
https://sourceforge.net/projects/xming/
- MongoDBCompass could be of help if you would like to connect to db with interface.
- Run commands in CMD line. Not in integratel terminal in VS-Code.


1. Start Xmimg: navigate to location of executable file and open with cmd: in my computer at "C:\Program Files (x86)\Xming"
"Xming.exe -ac"
2. If wanted: Start a MongoDB database in a container on a machine.
    2.1 Run database/container: "docker run --name mongodb -p 27017:27017 -d --network="networkone" mongodb/mongodb-community-server:latest"
    2.2 It is also possible to run mongodb locally not in a container. Anyhow, container use is recommended.

3. Build Docker images. Navigate to Container folder:
go following cmd: 
    --"docker build -t backend_image -f Dockerfileemail ." (This takes ~2mins on my machine)
    --"docker build -t gui_image -f Dockerfilegui ."


4. Set display variabel to host address in terminal that will have next command. (Must go to ipconf and find machines ip address. Use the IP address at Ethernet part.)
Add: ":0.0" After IP address, as seen in personal case below:
set DISPLAY=172.20.16.1:0.0

5. Run frontend to add and delete users. 
docker run -it --rm -e DISPLAY=%DISPLAY% --network="networkone" --name gui_container gui_image
this should start the frontend in the Xming window.
Now you can normally add and delete users. Whenever you are done, you can close the Xming window.


6. Start backend by running the backend image. ( -it flag will show you the output from print statements)
"docker run --rm --network=networkone --name backend_container -v /usr/share/zoneinfo/America/New_York:/etc/localtime:ro backend_image"

This includes setting the time zone within the Docker container to New_York.

This runs in the background. To stop it, you can either run docker stop INSERTDOCKERID
or open docker desktop GUI and stop through there


run a Docker container and see the print statements:
(Formal name: run in interactive environment)

 - docker run -t -i --network=networkone --name backend_container backend_image
 - docker run --rm -it --network=networkone --name backend_container -v /etc/localtime:/etc/localtime:ro backend_image

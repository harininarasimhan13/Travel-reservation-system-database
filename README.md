
README - Go2 Travel Reservation Service
SETUP AND INSTALLATION

To run the primary GUI script, the Python modules “tkinter” and “mysql.connector” must be installed. 
Installation of these modules vary by operating system and package manager (i.e. pip, conda, brew, etc.). 
MySQL must be installed on the user's system. Installation varies by operating system
Run trs_database.sql script on MySQL server and ensure that database was created on the server. This can be easily done through MySQL workbench.
Run trs_procedures.sql script on MySQL server and ensure that stored procedures and views were created on the server. This can be easily done through MySQL workbench.
To connect GUI to MySQL database and server, user must open trs_gui.py and input their MySQL host and user IDs, as well as their root password. This section can be found between lines 14 and 20:
#connect to mysql server
cnx = mysql.connector.connect(
   	host="localhost",  #hostname goes here
    	user="root",	#user ID goes here
    	password="password",  #password goes here
    	database="travel_reservation_service"
)
Make sure trs_gui.py is executable. This can be done by opening terminal application (bash, zsh, or other CLI applications should be sufficient) and typing chmod u+x trs_gui.py. 

RUNNING GO2 TRAVEL RESERVATION SERVICES

Open terminal application (bash, zsh, or other CLI applications should be sufficient) and type ./trs_gui.py (this will work if the file to execute is in the current path). 
This will open to the Login Page.
Here, users will provide login information or choose to register. 
If a user logs in, the program will detect if they are a customer, owner, or admin, and direct the user to the appropriate home page. 
If the user is both a customer and client, they will be asked if they would like to go to customer home or owner home page.

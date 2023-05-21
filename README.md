# flight-booking-system-devrev


## Round 2 TASK OF DEVREV

## HOSTED WEBSITE
### The website is hosted at https://flight-booking-system-devrev.onrender.com
##### Note: This web application was designed for desktop.


## ADMIN LOGIN CREDENTIALS
#### username - 'admin'
#### password - 'admin'

## ENDPOINTS

#### user login - /login
#### user register - /register
#### admin login - /admin-login

## SETUP

#### Step 1: Clone the repository using the command 'git clone https://github.com/Joshua-David1/flight-booking-system-devrev.git'
#### STEP 2: navigate to the directory 'flight-booking-system-devrev'
#### STEP 3: Install the necessary packages using the command 'pip install -r requirements.txt'.
#### STEP 4: Setup the environment variable for database url using the command 'export DATABASE_URL=sqlite:///<db-name>'.
#### STEP 5: After the packages have been installed and the environment variables have been set, the web server could be started with the command 'python server.py'.
#### STEP 6: The web application would be running on port 5000 and you could visit the web page using the url "http://localhost:5000"


## WEB APPLICATION

A login page is separately designed for Normal Users and admin.

### HOME PAGE
![home](https://github.com/Joshua-David1/flight-booking-system-devrev/assets/69303816/12b4d232-aa04-4131-ac76-59560ca800e5)
### REGISTER PAGE
![register](https://github.com/Joshua-David1/flight-booking-system-devrev/assets/69303816/74bcb323-6df4-4f36-9621-9a1fccaafa1a)
### LOGIN PAGE
![login](https://github.com/Joshua-David1/flight-booking-system-devrev/assets/69303816/64041dad-12fc-425b-af00-6e6c975cbb9e)
### ADMIN LOGIN PAGE
![admin-login](https://github.com/Joshua-David1/flight-booking-system-devrev/assets/69303816/da8e37d3-39c2-4a47-8c7c-a81638539b3f)

Users cannot login at admin login, and admin cannot login at user login.


### REGISTERING A USER
![login-cred](https://github.com/Joshua-David1/flight-booking-system-devrev/assets/69303816/429ffcb5-9ca4-4cda-8a5c-ebe19dac9f30)

A user named test10 with a password 'test10' is created in the above screenshot.
### USER DASHBOARD
![user-dashboard](https://github.com/Joshua-David1/flight-booking-system-devrev/assets/69303816/a947f378-bb0c-4679-be61-17b304551325)
In the user dashboard is where the flights booked by the user would be displayed.

### AVAILABLE FLIGHTS

![available-flights](https://github.com/Joshua-David1/flight-booking-system-devrev/assets/69303816/629d8cae-ea95-4c25-ae71-2c4b02ae3216)

All the flights which are availble for booking will be displayed in this section.
The flight number along with source, destination and time and date of departure would be listed.

### SEARCHING FOR A FLIGHT WITH SOURCE AND DESTINATION

![search-flight](https://github.com/Joshua-David1/flight-booking-system-devrev/assets/69303816/75b7720a-e8a7-4efe-a6a1-3335ec401702)
 We could search for a flight with source and destination.
 
 ### AFTER BOOKING
 ![after-booking](https://github.com/Joshua-David1/flight-booking-system-devrev/assets/69303816/1416508d-6664-4484-b804-54184a53c8a8)

After booking, the flight would be displayed in the dashboard of the user. The user also has the ability to cancel their flight.

### ADMIN LOGIN

#### username for admin - 'admin', password - 'admin'

![admin-login](https://github.com/Joshua-David1/flight-booking-system-devrev/assets/69303816/2225db21-12c2-4d5f-9007-c388c1e2d998)
This is where the admin could login into

### ADMIN DASHBOARD

![admin-dashboard](https://github.com/Joshua-David1/flight-booking-system-devrev/assets/69303816/9a1b8e2b-f8de-402f-a75d-25f9aaa560fc)

This is where all the flights added by the admin would be available. Admin has the ability to see all the users who booked a particular flight and can cancel the flight anytime.

### ADD A FLIGHT

![add-flight-ui](https://github.com/Joshua-David1/flight-booking-system-devrev/assets/69303816/879e2592-b431-4aac-9a65-3fe6deb30327)


### FLIGHT DETAILS TO ADD

![before-add-flight](https://github.com/Joshua-David1/flight-booking-system-devrev/assets/69303816/9cb493f7-9198-48d1-8ab9-cc535eda7b47)


### AFTER ADDING A NEW FLIGHT

![after-add-flight](https://github.com/Joshua-David1/flight-booking-system-devrev/assets/69303816/8b05f831-5638-4de9-ad7c-ca3912369329)

After entering the details of the flight to add, it would be displayed in the admin dashboard along with all the other flights.


If we want to take a look at who all booked a particular flight, we could press the Booked Users button.
FLight Cancellation could also be done by the admin by click on the red button 'cancel flight'.

### CANCELLING A FLIGH
![after-flight-cancel](https://github.com/Joshua-David1/flight-booking-system-devrev/assets/69303816/a283ab4b-c494-49f9-9bfb-3291b5b47674)
 Flight 90d has been canceled.


### BOOKED USERS

![booked-users](https://github.com/Joshua-David1/flight-booking-system-devrev/assets/69303816/b410bb2b-6e94-47af-80d4-fdd9ea200ff9)


## HOSTED WEBSITE

### The website is hosted at - https://flight-booking-system-devrev.onrender.com/
##### Note: This web application was designed for desktop.

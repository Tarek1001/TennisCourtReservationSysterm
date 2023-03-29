# Tennis Court Reservation Systerm
#### tarektouma98@gmail.com
The Tennis Court Reservation System is a platform for reserving tennis courts at a club or facility. The system allows users to view court availability and book a court for a specific date and time.
##### Installation
As no specific packages are required you should able to import all mentioned ones, but Python3 is required.

##### Usage
Enter your name the date and time you would like to reserve the court for.

##### Features
    -> Make a reservation
    -> Cancel a reservation
    -> Show Schedule
    -> Save Schedule in csv or json file
After each action you will receive a feedback about the reservation status, also program may offer different time in case of unavailability.
##### Limitations
1. you can NOT cancel a reservation if it only one hour or less from now.<br />
2. Maximum 2 reservation per person in week*.<br />
3. you can NOT make a reservation if it only one hour or less from now.<br />
###### *(week is from Monday to Sunday)
##### Interface
GUI is located is TennisCourtReservationGUI written using tkinter module<br /><br />
![alt text](https://github.com/Tarek1001/TennisCourtReservationSysterm/blob/main/Screenshot%20from%202023-03-29%2014-20-22.png?raw=true)

##### Database
The program use a json file a it's databese, you need to set the path in TennisCourtReservation to your file or just create a json file and name it 'schedule.json'



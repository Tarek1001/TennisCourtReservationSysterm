import tkinter as tk
from tkinter import*
from tkinter.ttk import Combobox
import tkinter.messagebox
from TennisCourtReservation import TennisCourtReservation
from datetime import datetime,timedelta,date
class TennisCourtReservationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tennis Court Reservation")
        self.tennis_court_reservation = TennisCourtReservation()
        #data
        period=(30,60,90)
        # Labels
        tk.Label(self.root, text="Name:").grid(row=0, column=0)
        tk.Label(self.root, text="Date (DD.MM.YY):").grid(row=1, column=0)
        tk.Label(self.root, text="Start Time (HH:MM):").grid(row=2, column=0)
        tk.Label(self.root, text="Period:").grid(row=3, column=0)

        # Entry fields
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=1, column=1)
        self.start_time_entry = tk.Entry(self.root)
        self.start_time_entry.grid(row=2, column=1)
        self.end_time_entry = Combobox(self.root, state="readonly", values=period,width=18)
        self.end_time_entry.grid(row=3, column=1)

        # Make reservation button
        tk.Button(self.root, text="Make Reservation", command=self.make_reservation_GUI).grid(row=5, column=0)
        # Cancel reservation  button
        tk.Button(self.root, text="Cancel Reservation", command=self.cancel_reservation_GUI).grid(row=5, column=1)
        # Download button
        tk.Button(self.root, text="Save Schedule", command=self.save_schedule_GUI).grid(row=6, column=0)
        # Show button
        tk.Button(self.root, text="Show Schedule", command=self.show_schedule_GUI).grid(row=6, column=1)
    
    def make_reservation_GUI(self):
        name = self.name_entry.get()
        date = self.date_entry.get()
        start_time = self.start_time_entry.get()
        try:
            period = int(self.end_time_entry.get())
            self.tennis_court_reservation.make_reservation(name,date,start_time,period)
            tkinter.messagebox.showinfo(title=None, message=self.tennis_court_reservation.reservationmessage)
            if self.tennis_court_reservation.check==False and self.tennis_court_reservation.doublecheck==True:
                self.alternative_GUI() 
        except Exception as e:
       	    print(e)
            tkinter.messagebox.showwarning(title=None, message="Correct input data")
                  
    def alternative_GUI(self):
        #Sub window 
        alternative_window = tk.Toplevel(self.root)
        alternative_window.title("Alternative reservation")
        alternative_window.geometry("450x125")
        
        name = self.name_entry.get()
        date = self.date_entry.get()
        start_time = self.start_time_entry.get()
        try:
            period = int(self.end_time_entry.get())
            self.tennis_court_reservation.alternative(date,start_time,period)
            label = tk.Label(alternative_window, text=self.tennis_court_reservation.alternativemessage
                             +" perss Confirm to make a reservation!")
            label.pack(padx=10, pady=10)

        except Exception as e:
       	    print(e)
            tkinter.messagebox.showwarning(title=None, message="Correct input data")
        def new_command():
                return self.tennis_court_reservation.make_reservation(name,date,
                                                           self.tennis_court_reservation.
                                                                       new_time.strftime('%H:%M'),period)

        def exit_btn():
            alternative_window.destroy()
        # button
        ok_button = tk.Button(alternative_window, text="Confirm", command=new_command)
        ok_button.pack(side=tk.RIGHT, padx=5, pady=10)
        cancel_button = tk.Button(alternative_window, text="Cancel", command=exit_btn)
        cancel_button.pack(side=tk.LEFT, padx=5, pady=10)

    def cancel_reservation_GUI(self):
        name = self.name_entry.get()
        date = self.date_entry.get()
        start_time = self.start_time_entry.get()
        try:
            period = int(self.end_time_entry.get())
            end_time=datetime.strptime(f"{date} at {start_time}",'%d.%m.%y at %H:%M')+timedelta(minutes=period)
            self.tennis_court_reservation.cancel_reservation(name,date,start_time,end_time.strftime('%H:%M'))
            tkinter.messagebox.showinfo(title=None, message=self.tennis_court_reservation.cancelmessage)
        except Exception as e:
       	    print(e)
            tkinter.messagebox.showwarning(title=None, message="Correct input data")
        
    def show_schedule_GUI(self):
        show_window = tk.Toplevel(self.root)
        show_window.title("Schedule")
        show_window.geometry("250x325")
        label = Label(show_window, text=self.tennis_court_reservation.show_schedule())
        label.pack()
        
        def exit_btn():
            show_window.destroy()
        # button
        cancel_button = tk.Button(show_window, text="Cancel", command=exit_btn)
        cancel_button.pack(side=tk.BOTTOM, padx=5, pady=10)
        
    def save_schedule_GUI(self):
        save_window = tk.Toplevel(self.root)
        save_window.title("Save schedule")
        save_window.geometry("250x125")
        
        def exit_btn():
            save_window.destroy()
  
        label = tk.Label(save_window, text="Do you want to save your data?")
        label.pack(padx=10, pady=10)
        #Save buttons
        json_button = tk.Button(save_window, text="JSON",  command=self.tennis_court_reservation.save_schedule('.json'))
        json_button.pack(side=tk.LEFT, padx=5, pady=10)
        csv_button = tk.Button(save_window, text="CSV", command=self.tennis_court_reservation.save_schedule('.csv'))
        csv_button.pack(side=tk.LEFT, padx=5, pady=10)
        cancel_button = tk.Button(save_window, text="Cancel", command=exit_btn)
        cancel_button.pack(side=tk.RIGHT, padx=5, pady=10)

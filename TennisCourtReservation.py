import json
from datetime import datetime,timedelta,date
from functools import reduce
import time
import calendar
import csv

class TennisCourtReservation():
    def __init__(self):
        self.filename='schedule.json' #data base
        self.reservations={}
        self.week_dictionary={}
        self.message=""
        self.cancelmessage=""
        self.reservationmessage=""
        self.alternativemessage=""
        self.check=False       #Use this variable to verify reservation.
        self.doublecheck=False #Use this variable to give an alternative time.
        self.player_starts=datetime.strptime("00:00",'%H:%M')
        self.player_ends=datetime.strptime("00:00",'%H:%M')
        self.new_time=datetime.strptime("00:00",'%H:%M')
        self.players_this_week=[]
        if open(self.filename, 'r'):
            with open(self.filename,'r') as f:
                self.schedule = json.load(f)
                f.close()
    def reset(self):
        self.__init__()

    #load data form the schedule
    def reservations_schedule(self):
        for date, reservations in self.schedule.items():
            user = [[
                    reservation['name'],
                    reservation['start_time'],
                    reservation['end_time']] for reservation in reservations]
            self.reservations.setdefault(date,[]).extend(user)
        return self.reservations
    
    #load users in each week
    def week_schedule(self):
        self.reset()
        for date, reservations in self.schedule.items():
            w=datetime.strptime(f"{date}",'%d.%m.%y').isocalendar().week
            names = [reservation['name'] for reservation in reservations]
            self.week_dictionary.setdefault(w,[]).append(names)
        return self.week_dictionary


    #Time checking
    def booking(self,date,time,period):
        reservations_schedule = self.reservations_schedule()
        reservation = datetime.strptime(f"{date} at {time}", '%d.%m.%y at %H:%M')
        #Reservation time cannot be less than one hour from now.
        if reservation <= datetime.now()+timedelta(minutes=60):
            self.message=f"Sorry, {reservation} is unavailable, try later date!"
            self.check=False
            self.doublecheck=False
        else:
            self.player_starts = reservation
            self.player_ends   = reservation + timedelta(minutes=period)
            try:
                day_schedule=reservations_schedule[date]
                #Empty day 
                if len(day_schedule)==0:
                    self.message="wait..."
                    self.check=True
                    self.doublecheck=False 
                #Reservation time cannot be unavaliable.
                for time in day_schedule:
                    start = datetime.strptime(f"{date} at {time[1]}", '%d.%m.%y at %H:%M')
                    end   = datetime.strptime(f"{date} at {time[2]}", '%d.%m.%y at %H:%M')
                    if  start <=  self.player_starts <= end  or\
                        start <=  self.player_ends <= end or\
                        (start >=  self.player_starts and self.player_ends >= end):
                        self.message=f"Sorry, Could not book on {date} form "\
                        f"{self.player_starts.time()} to {self.player_ends.time()}."
                        self.check=False
                        self.doublecheck=True 
                        break    
                    else:
                        self.message="wait..."
                        self.check=True
                        self.doublecheck=False
            except :# New day on schedule
                reservations_schedule[date]=[None]
                self.message="wait..."
                self.check=True
                self.doublecheck=False
        return self.check,self.message,self.player_starts,self.player_ends
    
    def make_reservation(self,name,date,time,period):
        new_reservation={}
        self.name = name
        self.date = datetime.strptime(f"{date}",'%d.%m.%y')
        self.time = datetime.strptime(f"{time}",'%H:%M')
        self.period=period
        self.players_this_week=[]
        def all_lower(my_list):
            return [x.lower() for x in my_list]
             
        week_schedule = self.week_schedule()
        check,message,player_starts,player_ends=self.booking(date,time,period)
        try:
            current_week =  week_schedule[self.date.isocalendar().week]
            self.players_this_week =all_lower (reduce(lambda z, y :z + y,current_week)) #return names as lower case
        except:#week without reservations!
            week_schedule[self.date.isocalendar().week] = []
            self.players_this_week=[]
        if self.players_this_week.count(name.lower())<2 :#compare users in each week with name, all in lower case.
            if check==True:
                self.reservationmessage=(f"Booking for {name} has been conformed on {date} from "
                        f"{player_starts.strftime('%H:%M')} to {player_ends.strftime('%H:%M')}.")
                new_reservation={"name": name,"start_time":time ,"end_time":player_ends.strftime('%H:%M')}
                self.schedule.setdefault(date,[]).append(new_reservation)
                self.write2file()
            else:
                self.reservationmessage=message
        else:
            self.reservationmessage="Sorry, maximum 2 reservations per person in one week!"
            self.doublecheck=False
    #Save new data to the data base.   
    def write2file(self):
    	#Sort by dates "keys"
        sorted_dates = sorted(self.schedule.keys(), key=lambda x: datetime.strptime(x, '%d.%m.%y'))
        keys_dictionary = dict.fromkeys(sorted_dates, None)
        for date in self.schedule:
        	#sort by start time.
            self.schedule[date].sort(key=lambda x: datetime.strptime(x['start_time'], '%H:%M'))
        sorted_schedule = {**keys_dictionary,**self.schedule}
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(sorted_schedule, f,indent=4,ensure_ascii=False)
            f.close()
        
    def cancel_reservation(self,name,date,start_time,end_time):
        self.name=name
        self.date=date
        self.start_time=start_time
        self.end_time=end_time
        case={}
        new_schedule=[]
        canceled_reservation={date:[name,start_time,end_time]}
        reservations_schedule = self.reservations_schedule()
        if datetime.strptime(f"{date} at {start_time}",'%d.%m.%y at %H:%M')>=datetime.now()+timedelta(minutes=60):
            for reservation in reservations_schedule[date]:
                if reservation==canceled_reservation[date]:
                    reservations_schedule[date].remove(reservation)
                    self.cancelmessage="Reservation has been canceled!.."
                    break
                else:
                    self.cancelmessage="No such a reservation in the system!.."
                case={"name": reservation[0],
                        "start_time":reservation[1] ,
                        "end_time":reservation[2]}
                new_schedule.append(case)
            self.schedule.update({date:new_schedule})
            self.write2file()
            #day dosenot exist
            if len(reservations_schedule[date])==0:
                 self.cancelmessage="No such a reservation in the system!.."
        
        else:
            self.cancelmessage="Can not cancel reservation now..!"
        return  self.cancelmessage              

    def show_schedule(self):
        today = date.today()
        show_message=""
        def show(day_message):
            text=""
            text+=(day_message+"\n")
            if len(self.schedule[day]) != 0:
                for player in self.schedule[day]:
                    text+="* {}  {}  {}\n".format(*player.values())
            else:
                text+=("No Reservations"+"\n")
            return text
        for day in self.schedule.keys():
            
            days=datetime.strptime(day,"%d.%m.%y").date()
            if days==today:
                show_message+=show("Today")
            elif days==today+timedelta(days=1):
                show_message+=show("Tomorrow")
            elif days>today+timedelta(days=1) and days<=today+timedelta(days=7):#show up to week
                show_message+=show(calendar.day_name[days.weekday()])
            else:
                pass
        return show_message
               
    def save_schedule(self,filetype):
        self.filetype=filetype
        save_message=""
        if filetype==".csv":
            header = ['name', 'start_time', 'end_time']
            data=[]
            reservations_schedule = self.reservations_schedule()
            for date,players in reservations_schedule.items():
                for player in players:
                    data.append([player[0],date+" "+player[1],date+" "+player[2]])
            with open('schedule.csv', 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(data)
            f.close()
        elif filetype==".json":
            self.write2file()
        else:
            save_message=("Error! unsupported file type!...")
            
    def alternative(self,date,time,period):
        old_time=datetime.strptime(f"{date} at {time}",'%d.%m.%y at %H:%M')
        n=0
        while(True):
            n+=15
            time_change = timedelta(minutes=n)
            self.new_time = time_change + old_time
            check,message,player_starts,player_ends=self.booking(date, self.new_time.strftime('%H:%M'),period)
            if check==True:
                self.alternativemessage=(f"You can pick { self.new_time.strftime('%d.%m.%y at %H:%M')}")
                break
        return self.alternativemessage, self.new_time


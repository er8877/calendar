from datetime import datetime
from tkinter import *
from tkcalendar import Calendar
import tkinter.ttk as ttk
import math
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import tkinter as tk
from PIL import ImageTk, Image
import requests
import pytz

try:
    
    response = requests.get('https://freegeoip.app/json/')
    if response.status_code == 200:
        data = response.json()
        current_city = data['city']
        
except NameError:
    print("check your connection !!!")
    
    
    
def get_current_location():
    global city
    try:
        response = requests.get('https://freegeoip.app/json/')
        if response.status_code == 200:
            data = response.json()
            city = data['city']
            return data['latitude'], data['longitude'] 
        else:
            print("Failed to retrieve location. Status code:", response.status_code)
    except Exception as e:
        print("An error occurred:", e)
        
        


def get_points(d_city):
    geolocator = Nominatim(user_agent="my_app")
    location = geolocator.geocode(d_city)
    if location:
        return location.latitude, location.longitude



def find_angles(target_city):
    your_location = get_current_location()
    your_location = (your_location[0], your_location[1])
    target_location = get_points(target_city)
    target_location = (target_location[0], target_location[1])

    if your_location is None or target_location is None:
        print("Error: Unable to find location for one or both cities.")
        return None
    
    distance = geodesic((your_location), (target_location)).kilometers
    delta_y = target_location[1] - your_location[1]
    delta_x = target_location[0] - your_location[0]

    bearing = math.degrees(math.atan2(delta_x, delta_y))

    if bearing < 0:
        bearing += 360
    
    return bearing, distance
    
    
    

def classify_direction(angle):
    directions = ["North", "Northeast", "East", "Southeast", 
                  "South", "Southwest", "West", "Northwest"]

    index = round(angle / (360. / len(directions))) % len(directions)
    
    return directions[index]




def calculate_destination_direction(destination):
    global combobox_destination_city
    d_city = get_points(destination)
    
    angle_c_d = find_angles(destination)[0]
    angle_c_d_1=find_angles(destination)[1]

    classify_dirs = classify_direction(angle_c_d)

    r = tk.Toplevel()
    r.geometry("928x576")
    r.title("result page")
    canvas= Canvas(r, width= 928, height= 576)
    canvas.pack()
    #Load an image in the script
    img= ImageTk.PhotoImage(Image.open("island.jpg"))
    #Add image to the Canvas Items
    canvas.create_image(0,0,anchor=NW,image=img)

    label_result_1 = tk.Label(r, text=f"Target city : {combobox_destination_city.get()} ", bg="#27187E", fg="#AEB8FE", font=("Arial", 25))
    label_result_1.place(x=30, y=110)
    label_result_2 = tk.Label(r, text=f"Direction : {classify_dirs} ", bg="#27187E", fg="#AEB8FE", font=("Arial", 25))
    label_result_2.place(x=30, y=170)
    label_result_3 = tk.Label(r, text=f"Distance : {int(angle_c_d_1)} kilometers ", bg="#27187E", fg="#AEB8FE", font=("Arial", 25))
    label_result_3.place(x=30, y=240)
    label_result_3 = tk.Label(r, text=f"Current city : {city} ", bg="#27187E", fg="#AEB8FE", font=("Arial", 25))
    label_result_3.place(x=30, y=50)
    r.mainloop()

    return classify_dirs, angle_c_d_1



def get_timezones(place_name):
    timezone = pytz.timezone(place_name)
    current_timezone = datetime.now(timezone)
    
    date_str = current_timezone.strftime("%Y / %m / %d")   
    time_str = current_timezone.strftime("%H : %M")
    
    date_label.config(text=date_str)
    time_label.config(text=time_str)
    


def pytz_timezone():
    global date_label, time_label
    
    timezone_win = tk.Toplevel()
    timezone_win.geometry("600x600")
    timezone_win.configure(background="#AEB8FE")
    timezone_win.title("time zone")
    
    border_page = Label(timezone_win, bg="#7F00FF", font=("Calibri (Body)", 16), fg="#F1F2F6", width=35, height=20)
    border_page.place(x=70, y=25)
    
    date = Label(timezone_win, text="Time zones", bg="#27187E", font=("Arial", 25), fg="#F1F2F6")
    date.place(x= 220, y=40)
    
    city_title = Label(timezone_win, text=" cities : ", bg="#27187E", font=("Calibri (Body)", 16), fg="#F1F2F6")
    city_title.place(x= 90, y=195, height=40, width=70)
    
    border_combobox = Label(timezone_win, bg="#27187E", font=("Arial", 16), fg="#F1F2F6")
    border_combobox.place(x= 190, y=190, height=55, width=260)
    
    exit_button = Button(timezone_win, text="Exit", bg="#27187E", font=("Arial", 16), fg="#F1F2F6", command=timezone_win.destroy)
    exit_button.place(x= 90, y=40, height=30, width=70)
    
    timezones_combobox = ttk.Combobox(timezone_win, values=list(pytz.all_timezones), font=("Arial", 15))
    timezones_combobox.place(x=200, y=200, width=240, height=35)
    
    timezone_button = Button(timezone_win, text="Get Timezone", bg="#27187E", font=("Arial", 16), fg="#F1F2F6", 
                             command=lambda:get_timezones(timezones_combobox.get()))
    timezone_button.place(x= 230, y=290, height=40, width=150)
    
    date_title_label = Label(timezone_win, text=" Date : ", bg="#27187E", font=("Calibri (Body)", 16), fg="#F1F2F6")
    date_title_label.place(x=90, y=400)
    
    date_label = Label(timezone_win, text="", bg="#27187E", font=("Calibri (Body)", 16), fg="#F1F2F6", width=21)
    date_label.place(x= 190, y=400 )
    
    time_title_label = Label(timezone_win, text=" Time : ", bg="#27187E", font=("Calibri (Body)", 16), fg="#F1F2F6")
    time_title_label.place(x=90, y=460)
    
    time_label = Label(timezone_win, text="", bg="#27187E", font=("Calibri (Body)", 16), fg="#F1F2F6", width=21)
    time_label.place(x= 190, y=460)
    
    timezone_win.mainloop()
    
    
    
    

date = datetime.now()
date_year = int(date.strftime("%Y"))
date_month = int(date.strftime("%m"))
date_day = int(date.strftime("%d"))

root = Tk()
root.geometry("600x600")
root.configure(background="#AEB8FE")
root.title("calendar")

border_combo = Label(root, bg="#27187E", font=("Arial", 16), fg="#F1F2F6")
border_combo.place(x= 241, y=410, height=55, width=265)
combobox_destination_city = ttk.Combobox(root, font=("Arial", 15), values=["Tehran", "Mashhad", "Isfahan", "Tabriz", "Shiraz", "Ahvaz", "Qom", "Kahriz", "Kermanshah",
               "Urmia", "Zahedan", "Qazvin", "Kerman", "Ardabil", "Rasht", "Sari", "Arak", "Bandar Abbas",
               "Yasuj", "Abadan", "Bojnourd", "Dezful", "Birjand", "Ilam", "Zanjan", "Malayer", "Saveh", 
               "Shahrud", "Mahabad", "Bandar-e Anzali", "Yazd", "Babol", "Borujerd", "Semnan", "Gonbad-e Kavus",
               "Varamin", "Gorgan", "Quchan", "Hamadan", "Maragheh", "Shahrekord", "Ghaemshahr", "Shahroud", 
               "Masjed Soleyman", "Shushtar", "Ramsar", "Behbahan", "Tonekabon", "Borazjan", "Bastam"], height=6)
combobox_destination_city.place(x=250, y=420)

t_city = Label(root, text="Target city : ", bg="#27187E", font=("Arial", 16), fg="#F1F2F6")
t_city.place(x= 85, y=420)

accept_button = Button(root, text="Accept", bg="#27187E", font=("Arial", 15), fg="#F1F2F6", activebackground="black", activeforeground="white",
                        command=lambda:calculate_destination_direction(combobox_destination_city.get()))
accept_button.place(x=241, y=550, width=100, height=35)

timezone_button = Button(root, text=" Time zones ", bg="#27187E", font=("Arial", 15), fg="#F1F2F6", activebackground="black", activeforeground="white",
                        command=pytz_timezone)
timezone_button.place(x=415, y=15, width=105, height=35)


date = Label(root, text="Calendar", bg="#27187E", font=("Arial", 25), fg="#F1F2F6")
date.place(x= 240, y=7)

current_city_lbl = Label(root, text=f"Current city :", bg="#27187E", font=("Arial", 16), fg="#F1F2F6")
current_city_lbl.place(x= 85, y=480)
current_city_text = Label(root, text=f"{current_city}", bg="#27187E", font=("Arial", 16), fg="#F1F2F6")
current_city_text.place(x= 241, y=480)

# Create a custom style for the calendar
style = ttk.Style()
style.theme_use('winnative')  # Change the theme if needed

# Configure the colors for different parts of the calendar
style.map("TButton",
          background=[('active', 'black')],
          foreground=[('active', 'black')])

cal = Calendar(root, selectmode='day',
               year=date_year, month=date_month, day=date_day, background="#27187E", disabledbackground="black", bordercolor="black", 
               headersbackground="#FF8600", normalbackground="#758BFD", foreground='white', 
               normalforeground='#27187E', headersforeground='#27187E', font="Arial 17", locale='en_US')

cal.place(x=85, y=90)

def grab_date():
    date.config(text="Selected Date is: " + cal.get_date())

root.mainloop()
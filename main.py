import requests
from tkinter import *
from tkinter import messagebox
from peewee import *
from PIL import Image, ImageTk
from datetime import *

db = SqliteDatabase('weather-data.db')

class BaseModel(Model):
    class Meta:
        database = db

class Weather(BaseModel):
    weather_id = IntegerField(primary_key=True)
    weather_city = TextField()
    weather_temp = TextField()
    weather_lat = TextField()
    weather_lon = TextField()
    weather_day = TextField()
    weather_descri = TextField()
    weather_image = BlobField()

db.connect()
db.create_tables([Weather])

class WeatherGUI(Tk):
    
    def __init__(self, title, geometry, color, file_path, file_path2, file_path3):
        self.img_search = file_path
        self.img_particle = file_path2
        self.img_box = file_path3
        Tk.__init__(self)
        self.title(title)
        self.geometry(geometry)
        self.config(bg=color)
        self.img_searchFI = PhotoImage(file=self.img_search)
        self.img_particleFI = PhotoImage(file=self.img_particle)
        self.img_boxFI = PhotoImage(file=self.img_box)
        self.create_search_lables()
        

    def create_search_lables(self):
        


        def get_weather():

            
                    

            day_names = {
                    'Monday': 'دوشنبه',
                    'Tuesday': 'سه‌شنبه',
                    'Wednesday': 'چهارشنبه',
                    'Thursday': 'پنج‌شنبه',
                    'Friday': 'جمعه',
                    'Saturday': 'شنبه',
                    'Sunday': 'یک‌شنبه'
                }

            

            city = en_search.get()
            api_key = ''
            try:
                res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric').json()
                lat = res['coord']['lat']
                lon = res['coord']['lon']
                res_lang_fa = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&lang=fa&units=metric').json()
                
                
                if res_lang_fa['cod'] == 200:
                    icon = res_lang_fa['weather'][0]['icon']
                    self.photoIcon = ImageTk.PhotoImage(file=f'images/{icon}@2x.png')
                    iconWeather.config(image=self.photoIcon)
                    day = datetime.now().strftime('%A')
                    showDay.config(text=day_names[day])

                    self.temp = res_lang_fa['main']['temp']
                    Ltemp.config(text=self.temp)
                    
                    self.description = res_lang_fa['weather'][0]['description']
                    Ldis.config(text=self.description)

                    self.humi = res_lang_fa['main']['humidity']
                    Lhumi.config(text=self.humi)

                    self.pre = res_lang_fa['main']['pressure']
                    Lpre.config(text=self.pre)

                    self.wind = res_lang_fa['wind']['speed']
                    Lwind.config(text=self.wind)

                    Llat.config(text=lat,bg='#203243')

                    Llon.config(text=lon,bg='#203243')

                    main = res_lang_fa['weather'][0]['main']
                
                else:
                    messagebox.showerror('خطا', "خطا در وارد کردن اطلاعات")
            except:
                messagebox.showerror('خطا', "خطا در وصل شدن به سرور")

            finally:
                def image_to_binry(image):
                    with open(image, 'rb') as f:
                        image_data = f.read()

                    return image_data
                binery = image_to_binry(f'images/{icon}@2x.png')
                new_weather = Weather(weather_city = city,
                                      weather_temp = self.temp,
                                      weather_lat = lat,
                                      weather_lon = lon,
                                      weather_day = day,
                                      weather_descri = self.description,
                                      weather_image = binery)
                new_weather.save()
                messagebox.showinfo('دیتا بیس' , 'اطلاعات در دیتا بیس ذخیره شد')

        l = Label(self,
                  text='میتونید اسم شهر هارو به فارسی وارد کنید مثل : تهران',
                  font=('arial', 18, 'bold'),
                  bg='#89cff0',
                  fg='black')
        l.place(x=260, y=10)
        

        lb_search = Label(image=self.img_searchFI, bg='#89cff0')
        lb_search.place(x=270, y=80)

        lb_particle = Button(image=self.img_particleFI, bg='#203243', command=get_weather)
        lb_particle.place(x=630, y=82)

        en_search = Entry(self,
                           justify='center', 
                           bd=0,
                           bg='#203243',
                           fg='white',
                           font=('arial', 25, 'bold'),
                           width=15)
        en_search.place(x=350, y=90)
        en_search.focus()

        iconWeather = Label(self, bg='#89cff0', font=('arial', 20))
        iconWeather.place(x=450, y=220)


        showDay = Label(bg='#89cff0',font=('arial', 25, 'bold'))
        showDay.place(x=40, y=50)


        boxInfo = Label(image=self.img_boxFI, bg='#89cff0')
        boxInfo.place(x=30, y=110)

        l1 = Label(self,
                    text=':  دما', 
                    font=('arial', 11, 'bold'), 
                    fg='white', 
                    bg='#203243')
        l1.place(x=170, y=120)

        Ltemp = Label(self,
                    font=('arial', 11, 'bold'), 
                    fg='white', 
                    bg='#203243')
        Ltemp.place(x=50, y=120)

        l2 = Label(self,
                    text=':  رطوبت', 
                    font=('arial', 11, 'bold'), 
                    fg='white', 
                    bg='#203243')
        l2.place(x=160, y=140)

        Lhumi = Label(self,
                    font=('arial', 11, 'bold'), 
                    fg='white', 
                    bg='#203243')
        Lhumi.place(x=50, y=140)

        l3 = Label(self,
                    text=':  فشار', 
                    font=('arial', 11, 'bold'), 
                    fg='white', 
                    bg='#203243')
        l3.place(x=170, y=160)

        Lpre = Label(self,
                    font=('arial', 11, 'bold'), 
                    fg='white', 
                    bg='#203243')
        Lpre.place(x=50, y=160)

        l4 = Label(self,
                    text=':  سرعت باد', 
                    font=('arial', 11, 'bold'), 
                    fg='white', 
                    bg='#203243')
        l4.place(x=150, y=180)

        Lwind = Label(self,
                    font=('arial', 11, 'bold'), 
                    fg='white', 
                    bg='#203243')
        Lwind.place(x=50, y=180)

        l5 = Label(self,
                    text=':  شرح', 
                    font=('arial', 11, 'bold'), 
                    fg='white', 
                    bg='#203243')
        l5.place(x=170, y=200)

        Ldis = Label(self,
                    font=('arial', 11, 'bold'), 
                    fg='white', 
                    bg='#203243')
        Ldis.place(x=50, y=200)

        l6 = Label(self,
                    text=':  طول جغرافیایی', 
                    font=('arial', 11, 'bold'), 
                    fg='white', 
                    bg='#203243')
        l6.place(x=300, y=400)

        Llon = Label(self,
                    font=('arial', 11, 'bold'), 
                    fg='white', 
                    bg='#89cff0')
        Llon.place(x=200, y=400)

        l7 = Label(self,
                    text=':  عرض جغرافیایی', 
                    font=('arial', 11, 'bold'), 
                    fg='white', 
                    bg='#203243')
        l7.place(x=700, y=400)

        Llat = Label(self,
                    font=('arial', 11, 'bold'), 
                    fg='white', 
                    bg='#89cff0')
        Llat.place(x=600, y=400)

        lSaman = Label(self,
                       text='سامان قاسمی',
                       bg= '#89cff0',
                       fg='black',
                       font=('arial', 18, 'bold'))
        lSaman.place(x=40, y=300)
        

GUI = WeatherGUI('برنامه اب و هوایی',
                  '890x470', 
                  '#89cff0', 
                  'images/another/Rounded-Rectangle-3.png',
                  'images/another/Laye-6.png',
                  'images/another/Rounded-Rectangle-1.png')
GUI.mainloop()

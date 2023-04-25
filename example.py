import customtkinter
from tkintermapview import TkinterMapView
from PIL import Image, ImageTk
import tkinter
from pathlib import Path
import geopy.distance
from geopy import Point
from additional_functions import destination

customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):

    APP_NAME = "TkinterMapView with CustomTkinter"
    WIDTH = 800
    HEIGHT = 500

    def __init__(self,  icon: tkinter.PhotoImage = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)

        #self.marker_list = []

        # ============ create two CTkFrames ============

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, width=150, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============ frame_left ============

        self.frame_left.grid_rowconfigure(2, weight=1)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Clear Paths",
                                                command=self.clear_path_event)
        self.button_1.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Clear Markers",
                                                command=self.clear_marker_event)
        self.button_2.grid(pady=(20, 0), padx=(20, 20), row=1, column=0)
        self.var1 = tkinter.IntVar()
        self.var2 = tkinter.IntVar()
        self.var3 = tkinter.IntVar()
        self.button_3 = customtkinter.CTkCheckBox(master=self.frame_left, 
                                                  text = "visual",
                                                  command=self.add_marker_event,
                                                  variable=self.var1, onvalue=1, offvalue=0)
        self.button_3.grid(pady=(10, 0), padx=(0, 0), row=7, column=0)

        self.button_4 = customtkinter.CTkCheckBox(master=self.frame_left, 
                                                  text="inertio",
                                                  command=self.add_marker_event,
                                                  variable=self.var2, onvalue=1, offvalue=0)
        self.button_4.grid(pady=(10, 0), padx=(0, 0), row=8, column=0)
        
        self.button_6 = customtkinter.CTkCheckBox(master=self.frame_left, 
                                                  text="galileo",
                                                  command=self.add_marker_event,
                                                  variable=self.var3, onvalue=1, offvalue=0)
        self.button_6.grid(pady=(10, 10), padx=(0, 0), row=9, column=0)

        self.speed = customtkinter.CTkEntry(master=self.frame_left, placeholder_text="speed")
        self.speed.grid(pady=(10, 10), padx=(0, 0), row=10, column=0)

        self.time = customtkinter.CTkEntry(master=self.frame_left, placeholder_text="time diff")
        self.time.grid(pady=(10, 10), padx=(0, 0), row=11, column=0)

        self.map_label = customtkinter.CTkLabel(self.frame_left, text="Tile Server:", anchor="w")
        self.map_label.grid(row=3, column=0, padx=(20, 20), pady=(20, 0))
        self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["OpenStreetMap", "Google normal", "Google satellite", "Paint", "Black and White", "Terrain"],
                                                                       command=self.change_map)
        self.map_option_menu.grid(row=4, column=0, padx=(20, 20), pady=(10, 0))

        self.appearance_mode_label = customtkinter.CTkLabel(self.frame_left, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=(20, 20), pady=(20, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_left, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=(20, 20), pady=(10, 20))

        # ============ frame_right ============

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        self.map_widget = TkinterMapView(self.frame_right, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            placeholder_text="type address")
        self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        self.entry.bind("<Return>", self.search_event)

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Search",
                                                width=90,
                                                command=self.search_event)
        self.button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

        # Set default values
        self.map_widget.set_address("Thessaloniki")
        self.map_option_menu.set("OpenStreetMap")
        self.appearance_mode_optionemenu.set("Dark")
        self.new_marker_1 = []
        self.new_path_1 = []
        self.icon = icon
        self.filename = None
        self.d = 0
        self.P1 = []
        #self.tool = "visual"
        # self.map_widget.add_right_click_menu_command(label="Add Marker",
        #                                 command=self.add_marker_event,
        #                                 pass_coords=True)
        
    #def wait_click(self):
        self.map_widget.add_right_click_menu_command(label="Add Marker",
                                        command=self.add_marker_event,
                                        pass_coords=True)

    def search_event(self, event=None):
        self.map_widget.set_address(self.entry.get())

    #my addition

    def set_icon(self):
        #print("Speed ", self.speed.get())
        #print("time diff ", self.time.get())
        if (self.var1.get() == 1) & (self.var2.get() == 0) & (self.var3.get() == 0):
            self.filename = "./visual.png"
            self.icon = ImageTk.PhotoImage(Image.open(self.filename).resize((60, 60)))
            print(Path(self.filename).stem)
            return self.icon
        elif (self.var1.get() == 0) & (self.var2.get() == 1) & (self.var3.get() == 0):
            self.filename = "./inertio.png"
            self.icon = ImageTk.PhotoImage(Image.open(self.filename).resize((60, 60)))
            print(Path(self.filename).stem)
            return self.icon
        elif (self.var1.get() == 0) & (self.var2.get() == 0) & (self.var3.get() == 1):
            self.filename = "./gnss.png"
            self.icon = ImageTk.PhotoImage(Image.open(self.filename).resize((60, 60)))
            print(Path(self.filename).stem)
            return self.icon
        elif (self.var1.get() == 0) & (self.var2.get() == 0) & (self.var3.get() == 0):
            tkinter.messagebox.showwarning(title=None, message="No tool selected")
            self.clear_marker_event()
            self.clear_path_event()
            assert ((self.var1.get() == 1) or (self.var2.get() == 1) or (self.var3.get() == 1)), "No tool selected"
        else:
            tkinter.messagebox.showwarning(title=None, message="Multiple tools selected")
            self.clear_marker_event()
            self.clear_path_event()
            assert ((self.var1.get() == 1) and (self.var2.get() == 1) and (self.var3.get() == 1)), "Multiple tools selected"
            assert ((self.var1.get() == 1) and (self.var2.get() == 1) and (self.var3.get() == 0)), "Multiple tools selected"
            assert ((self.var1.get() == 1) and (self.var2.get() == 0) and (self.var3.get() == 1)), "Multiple tools selected"
            assert ((self.var1.get() == 0) and (self.var2.get() == 1) and (self.var3.get() == 1)), "Multiple tools selected"





    def add_marker_event(self, coords = (0,0)):
        print("Add marker:", coords)
        
        new_marker = self.map_widget.set_marker(coords[0], coords[1], text = "("+ str(coords[0]) +","+ str(coords[1])+")", font = "Tahoma 9", text_color = '#e61212', icon = self.set_icon()).position
        self.new_marker_1.append(new_marker)

        if (len(self.new_marker_1)>=3) and (len(self.P1)>=3) and (self.new_marker_1[-2][0] != 0) and (self.new_marker_1[1][0] != 0):
            distance = geopy.distance.geodesic(self.new_marker_1[-1], self.new_marker_1[-2]).km
            if distance + self.d == int(self.speed.get())/int(self.time.get()):
                self.P1.append(self.new_marker_1[-1])
                #print("P1 = ", P1)
                self.d = 0
            while distance + self.d > int(self.speed.get())/int(self.time.get()): #and self.d>10
                #print("d = ", self.d)
                endiameso_1 = destination(lat1 = self.new_marker_1[-2][0], long1 = self.new_marker_1[-2][1],
                                    lat2 = self.new_marker_1[-1][0], long2 = self.new_marker_1[-1][1],
                                    kms = int(self.speed.get())/int(self.time.get()) - self.d)
                self.new_marker_1.insert(-1, (float(endiameso_1.find_destination().split(",")[0]), float(endiameso_1.find_destination().split(",")[1])))
                self.P1.append(self.new_marker_1[-2])
                #distance = geopy.distance.geodesic(self.new_marker_1[-1], self.new_marker_1[-2]).km
                distance = geopy.distance.geodesic(self.new_marker_1[-1], self.new_marker_1[-2]).km
                self.d = 0
                #distance = distance - int(self.speed.get())/int(self.time.get()) # no
                #print(self.d)
                #print("distance", distance)
                #self.d = distance + self.d - int(self.speed.get())/int(self.time.get())
                #print("P1 = ", P1) 
                #print(endiameso.find_destination())
            if distance + self.d < int(self.speed.get())/int(self.time.get()):
                #P1 = self.new_marker_1[:-1]
                #print("P1 = ", P1)
                #self.new_marker_1.pop(-1)
                self.d = distance + self.d

        #I have already added two points on the map
        elif (len(self.new_marker_1)>=3) and (len(self.P1)<3) and (self.new_marker_1[-2][0] != 0) and (self.new_marker_1[-1][0] != 0):
            self.d = geopy.distance.geodesic(self.new_marker_1[-1], self.new_marker_1[-2]).km
            #print(self.d)
            if self.d < int(self.speed.get())/int(self.time.get()):
                self.P1 = [self.new_marker_1[1:]]
            if self.d == int(self.speed.get())/int(self.time.get()):
                self.P1 = self.new_marker_1[1:]
                #print("P1 = ", P1)
                self.d = 0
            while self.d > int(self.speed.get())/int(self.time.get()):
                endiameso = destination(lat2 = self.new_marker_1[-1][0], long2 = self.new_marker_1[-1][1],
                                    lat1 = self.new_marker_1[-2][0], long1 = self.new_marker_1[-2][1],
                                    kms = int(self.speed.get())/int(self.time.get()))
                print("Endiameso ", endiameso.find_destination())
                self.new_marker_1.insert(-1, (float(endiameso.find_destination().split(",")[0]), float(endiameso.find_destination().split(",")[1])))
                #P1 = self.new_marker_1.pop(-2)
                #print("P1 = ", P1)
                #self.d = self.d - int(self.speed.get())/int(self.time.get())
                #print(self.new_marker_1)
                self.d = geopy.distance.geodesic(self.new_marker_1[-1], self.new_marker_1[-2]).km
                self.P1 = self.new_marker_1[1:-1]
                #print(self.d)


        print("P1 = ", self.P1)
        print(self.new_marker_1)
        return self.d, self.new_marker_1, self.P1    
    ''''  
        if (len(self.new_marker_1)>1) and (self.new_marker_1[-2][0] != 0) and (self.new_marker_1[-1][0] != 0):
            distance = geopy.distance.geodesic(self.new_marker_1[-1], self.new_marker_1[-2]).km
            print(distance)
            if distance <= int(self.speed.get())/int(self.time.get()):
                new_path_short = self.map_widget.set_path([self.new_marker_1[-1], self.new_marker_1[-2]])
                #km = int(self.speed.get())/int(self.time.get()) - distance
            else:
                pass
        #Add the endiameso point between two points with larger distance than defined by users speed and time diff
            while distance > int(self.speed.get())/int(self.time.get()):
                km = int(self.speed.get())/int(self.time.get())
                endiameso = destination(lat1 = self.new_marker_1[-2][0], long1 = self.new_marker_1[-2][1],
                                    lat2 = self.new_marker_1[-1][0], long2 = self.new_marker_1[-1][1],
                                    kms = km)
                print("Endiameso ", endiameso.find_destination())
                endiam.append((float(endiameso.find_destination().split(",")[0]), float(endiameso.find_destination().split(",")[1])))
                self.new_marker_1.insert(-1, (float(endiameso.find_destination().split(",")[0]), float(endiameso.find_destination().split(",")[1])))
                #distance = abs(geopy.distance.geodesic(self.new_marker_1[-1], self.new_marker_1[-2]).km) #- geopy.distance.geodesic(self.new_marker_1[-2], self.new_marker_1[-3]).km)
                #distance = geopy.distance.geodesic(self.new_marker_1[-1], endiam[-1]).km
                new_path_long = self.map_widget.set_path([self.new_marker_1[-1], self.new_marker_1[-3]])
        #I have already added more than two points
                
                #print("endiam:", endiam)
                distance = geopy.distance.geodesic(self.new_marker_1[-1], self.new_marker_1[-2]).km
            
            if distance <= int(self.speed.get())/int(self.time.get()):
                dist = distance
                # distance = distance + geopy.distance.geodesic(self.new_marker_1[-1], self.new_marker_1[-2]).km
                # if (len(self.new_marker_1)>3) and (self.new_marker_1[-2][0] != 0) and (self.new_marker_1[-1][0] != 0):
                #     km = int(self.speed.get())/int(self.time.get()) - distance    
                #     endiameso = destination(lat1 = self.new_marker_1[-2][0], long1 = self.new_marker_1[-2][1],
                #                         lat2 = self.new_marker_1[-1][0], long2 = self.new_marker_1[-1][1],
                #                         kms = km)
                #     print("mikro endiam ", endiameso.find_destination())
                #     self.new_marker_1.insert(-1, (float(endiameso.find_destination().split(",")[0]), float(endiameso.find_destination().split(",")[1])))
                #     distance = geopy.distance.geodesic(self.new_marker_1[-1], self.new_marker_1[-2]).km
        # if (len(self.new_marker_1)>2) and (self.new_marker_1[-2][0] != 0) and (self.new_marker_1[-1][0] != 0):


        #     distance = geopy.distance.geodesic(self.new_marker_1[-1], self.new_marker_1[-2]).km
        #     print(distance)
        #     #new_path_short = self.map_widget.set_path([self.new_marker_1[-1], self.new_marker_1[-2]])
        #     #self.new_path_1.append(new_path)
        #     #print("Add path:", self.new_marker_1[-2] , "->", self.new_marker_1[-1])
        print(self.new_marker_1)
'''



    def clear_marker_event(self):
        for marker in self.new_marker_1:
            marker.delete()
        self.new_marker_1=[]


    def clear_path_event(self):
        for paths in self.new_path_1:
            paths.delete()

    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_map(self, new_map: str):
        if new_map == "OpenStreetMap":
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Google normal":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "Google satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "Paint":
            self.map_widget.set_tile_server("http://c.tile.stamen.com/watercolor/{z}/{x}/{y}.png",)
        elif new_map == "Black and White":
            self.map_widget.set_tile_server("http://a.tile.stamen.com/toner/{z}/{x}/{y}.png",)
        elif new_map == "Terrain":
            self.map_widget.set_tile_server("http://a.tile.stamen.com/terrain/{z}/{x}/{y}.png",)        

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        #self.wait_click()
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()


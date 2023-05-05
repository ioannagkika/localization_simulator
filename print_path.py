import customtkinter
from tkintermapview import TkinterMapView
from PIL import Image, ImageTk
import tkinter
from pathlib import Path
import geopy.distance
from geopy import Point
from additional_functions import destination
from tkintermapview.canvas_position_marker import CanvasPositionMarker
from set_path import wanted_marker
import sys

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

        self.clear = customtkinter.CTkButton(master=self.frame_left,
                                                text="Clear Markers",
                                                command=self.clear_marker_event, fg_color="red", hover_color="pink")
        self.clear.grid(pady=(20, 0), padx=(5, 5), row=3, column=0)

        self.broker_button = customtkinter.CTkEntry(master=self.frame_left, placeholder_text="Broker IP")
        self.broker_button.grid(pady=(10, 0), padx=(5, 5), row=0, column=0)

        self.datetime_button = customtkinter.CTkEntry(master=self.frame_left, placeholder_text="datetime")
        self.datetime_button.grid(pady=(10, 0), padx=(5, 5), row=1, column=0)

        self.fr_id_button = customtkinter.CTkEntry(master=self.frame_left, placeholder_text="FR ID")
        self.fr_id_button.grid(pady=(10, 0), padx=(5, 5), row=2, column=0, sticky = "n")   


        self.map_label = customtkinter.CTkLabel(self.frame_left, text="Tile Server:", anchor="w")
        self.map_label.grid(row=4, column=0, padx=(0, 0), pady=(20, 0))
        self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["OpenStreetMap", "Google normal", "Google satellite", "Paint", "Black and White", "Terrain"],
                                                                       command=self.change_map)
        self.map_option_menu.grid(row=5, column=0, padx=(0, 0), pady=(10, 0))

        self.appearance_mode_label = customtkinter.CTkLabel(self.frame_left, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=(0, 0), pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_left, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=(0, 0), pady=(10, 0))


        self.var1 = tkinter.IntVar()
        self.var2 = tkinter.IntVar()
        self.var3 = tkinter.IntVar()

        self.visual_button = customtkinter.CTkCheckBox(master=self.frame_left, 
                                                  text = "visual",
                                                  command=self.add_marker_event,
                                                  variable=self.var1, onvalue=1, offvalue=0)
        self.visual_button.grid(pady=(10, 0), padx=(0, 0), row=8, column=0)
        self.time_visual = customtkinter.CTkEntry(master=self.frame_left, placeholder_text="time diff")
        self.time_visual.grid(pady=(10, 0), padx=(10, 20), row=8, column=1)

        self.inertio_button = customtkinter.CTkCheckBox(master=self.frame_left, 
                                                  text="inertio",
                                                  command=self.add_marker_event,
                                                  variable=self.var2, onvalue=1, offvalue=0)
        self.inertio_button.grid(pady=(10, 0), padx=(0, 0), row=9, column=0)
        self.time_inertio = customtkinter.CTkEntry(master=self.frame_left, placeholder_text="time diff")
        self.time_inertio.grid(pady=(10, 0), padx=(10, 20), row=9, column=1)

        self.galileo_button = customtkinter.CTkCheckBox(master=self.frame_left, 
                                                  text="galileo",
                                                  command=self.add_marker_event,
                                                  variable=self.var3, onvalue=1, offvalue=0)
        self.galileo_button.grid(pady=(10, 0), padx=(0, 0), row=10, column=0)
        self.time_galileo = customtkinter.CTkEntry(master=self.frame_left, placeholder_text="time diff")
        self.time_galileo.grid(pady=(10, 0), padx=(10, 20), row=10, column=1)

        self.speed = customtkinter.CTkEntry(master=self.frame_left, placeholder_text="speed")
        self.speed.grid(pady=(10, 20), padx=(0, 0), row=11, column=0)




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

        self.button_8 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Search",
                                                width=90,
                                                command=self.search_event)
        self.button_8.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

        # Set default values
        self.map_widget.set_address("Thessaloniki")
        self.map_option_menu.set("OpenStreetMap")
        self.appearance_mode_optionemenu.set("Light")
        self.new_marker_1 = [] #list of every coordinate, both the ones added by the user and the wanted ones
        self.new_path_1 = []
        #self.icon = icon
        self.filename = "./visual.png"
        self.icon = ImageTk.PhotoImage(Image.open(self.filename).resize((60, 60)))
        #self.d = 0 #distance between two markers
        #self.P1 = [] #list of the wanted markers
        #self.l =[] #list that appends the distances between the markers that we have added until the sum of the distances gets the wanted value (speed * time diff)
        self.markers=[]
        self.map_widget.add_right_click_menu_command(label="Add Marker",
                                        command=self.add_marker_event,
                                        pass_coords=True)
        self.visual_marker = wanted_marker()
        self.inertio_marker = wanted_marker()
        self.galileo_marker = wanted_marker()

    def search_event(self, event=None):
        self.map_widget.set_address(self.entry.get())

  
# The user enters the path, P1 with the wanted coordinates is created
    def add_marker_event(self, coords = (0,0)):
        print("Add marker:", coords)
    
        new_marker = self.map_widget.set_marker(coords[0], coords[1], text = "("+ str(coords[0]) +","+ str(coords[1])+")", font = "Tahoma 9", text_color = '#e61212')#, icon = self.set_icon())
        #self.new_marker_1.append(new_marker.position)
        self.markers.append(new_marker)

        if (self.var1.get() == 1) & (self.var2.get() == 0) & (self.var3.get() == 0):
            #self.visual_marker = wanted_marker()
            self.visual_marker.new_marker_1.append(new_marker.position)
            self.visual_marker.set_marker(dt = self.time_visual.get(), speed = self.speed.get())

        elif (self.var1.get() == 0) & (self.var2.get() == 1) & (self.var3.get() == 0):
            #self.inertio_marker = wanted_marker()
            self.inertio_marker.new_marker_1.append(new_marker.position)
            self.inertio_marker.set_marker(dt = self.time_inertio.get(), speed = self.speed.get())

        elif (self.var1.get() == 0) & (self.var2.get() == 0) & (self.var3.get() == 1):
            #self.galileo_marker = wanted_marker()
            self.galileo_marker.new_marker_1.append(new_marker.position)
            self.galileo_marker.set_marker(dt = self.time_galileo.get(), speed = self.speed.get())

        elif (self.var1.get() == 0) & (self.var2.get() == 0) & (self.var3.get() == 0):
            tkinter.messagebox.showerror(title=None, message="No tool selected")
            sys.exit("No tool selected")
            # self.clear_marker_event()
            # self.clear_path_event()
            # assert ((self.var1.get() == 1) or (self.var2.get() == 1) or (self.var3.get() == 1)), "No tool selected"

        elif (self.var1.get() == 1) & (self.var2.get() == 1) & (self.var3.get() == 0):
            #self.visual_marker = wanted_marker()
            self.visual_marker.new_marker_1.append(new_marker.position)
            self.visual_marker.set_marker(dt = self.time_visual.get(), speed = self.speed.get())
            #self.inertio_marker = wanted_marker()
            self.inertio_marker.new_marker_1.append(new_marker.position)
            self.inertio_marker.set_marker(dt = self.time_inertio.get(), speed = self.speed.get())

        elif (self.var1.get() == 1) & (self.var2.get() == 0) & (self.var3.get() == 1):
            #self.visual_marker = wanted_marker()
            self.visual_marker.new_marker_1.append(new_marker.position)
            self.visual_marker.set_marker(dt = self.time_visual.get(), speed = self.speed.get())
            #self.galileo_marker = wanted_marker()
            self.galileo_marker.new_marker_1.append(new_marker.position)
            self.galileo_marker.set_marker(dt = self.time_galileo.get(), speed = self.speed.get())

        elif (self.var1.get() == 0) & (self.var2.get() == 1) & (self.var3.get() == 1):
            #self.inertio_marker = wanted_marker()
            self.inertio_marker.new_marker_1.append(new_marker.position)
            self.inertio_marker.set_marker(dt = self.time_inertio.get(), speed = self.speed.get())
            #self.galileo_marker = wanted_marker()
            self.galileo_marker.new_marker_1.append(new_marker.position)
            self.galileo_marker.set_marker(dt = self.time_galileo.get(), speed = self.speed.get())

        elif (self.var1.get() == 1) & (self.var2.get() == 1) & (self.var3.get() == 1):
            #self.visual_marker = wanted_marker()
            self.visual_marker.new_marker_1.append(new_marker.position)
            self.visual_marker.set_marker(dt = self.time_visual.get(), speed = self.speed.get())
            #self.inertio_marker = wanted_marker()
            self.inertio_marker.new_marker_1.append(new_marker.position)
            self.inertio_marker.set_marker(dt = self.time_inertio.get(), speed = self.speed.get())
            #self.galileo_marker = wanted_marker()
            self.galileo_marker.new_marker_1.append(new_marker.position)
            self.galileo_marker.set_marker(dt = self.time_galileo.get(), speed = self.speed.get())        


        
        


    def clear_marker_event(self):
        # for i in range(len(self.new_marker_1)):
        #     self.new_marker_1[i] = CanvasPositionMarker(position = self.new_marker_1[i], map_widget= "TkinterMapView")
        for marker in self.markers:    
            marker.delete()
        # self.new_marker_1.clear()
        self.markers = []

        self.visual_marker.P1.clear()
        self.visual_marker.d = 0
        self.visual_marker.l = []
        self.visual_marker.new_marker_1=[(0,0)]

        self.inertio_marker.P1.clear()
        self.inertio_marker.d = 0
        self.inertio_marker.l = []
        self.inertio_marker.new_marker_1=[(0,0)]

        self.galileo_marker.P1.clear()
        self.galileo_marker.d = 0
        self.galileo_marker.l = []
        self.galileo_marker.new_marker_1=[(0,0)]        


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


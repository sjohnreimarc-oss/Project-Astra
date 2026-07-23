import customtkinter as ctk
from PIL import Image
from assets.icons import PLANET_ICONS, UI_ICONS
from logic.orbital_mechanics_logic import OrbitalMechanicsLogic
from gui.orbital_mechanics_gui import OrbitalMechanicsGUI
from gui.interplanetary_gui import InterplanetaryGUI
from gui.mission_planning_gui import MissionPlanningGUI
from gui.rocketry_gui import RocketryGUI
from utils.helpers import resource_path

class ProjectAstraGUI(ctk.CTk):
    """GUI class for Project Astra."""
    def __init__(self):
        super().__init__()
        self.title("Project Astra")
        self.geometry("1500x850")
        ctk.set_appearance_mode("Dark")

        # Instantiate the Logic
        self.logic = OrbitalMechanicsLogic()

        # Initialize the Icons
        self.planet_icons = {}
        for body, path in PLANET_ICONS.items():
            self.planet_icons[body] = ctk.CTkImage(
                light_image=Image.open(resource_path(path)),
                dark_image=Image.open(resource_path(path)),
                size=(25,25))

        self.ui_icons = {}
        for name, path in UI_ICONS.items():
            self.ui_icons[name] = ctk.CTkImage(
                light_image=Image.open(resource_path(path)),
                dark_image=Image.open(resource_path(path)),
                size=(20, 20))

        #Set up the upper frame
        nav_frame = ctk.CTkFrame(self, height=70, fg_color="transparent")
        nav_frame.pack(fill="x", pady=5)
        nav_frame.pack_propagate(False)
        nav_frame.grid_columnconfigure(0, weight=2)
        nav_frame.grid_columnconfigure(1, weight=4)
        nav_frame.grid_columnconfigure(2, weight=1)

        left_nav_frame = ctk.CTkFrame(nav_frame, fg_color="transparent")
        center_nav_frame = ctk.CTkFrame(nav_frame, fg_color="transparent")
        right_nav_frame = ctk.CTkFrame(nav_frame, fg_color="transparent")

        left_nav_frame.pack(side="left", padx=20)
        center_nav_frame.pack(side="left", fill="x", expand=True, padx=20)
        right_nav_frame.pack(side="right", padx=20)
        center_nav_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        center_nav_frame.grid_rowconfigure(0, weight=1)

        title_label_1 = ctk.CTkLabel(left_nav_frame,
                                     text=" Project Astra",
                                     image=self.ui_icons.get("rocket"),
                                     compound="left",
                                     font=ctk.CTkFont(size=18, weight="bold"))
        title_label_2 = ctk.CTkLabel(left_nav_frame, text="Astrodynamics Toolkit", font=ctk.CTkFont(size=12))
        title_label_1.grid(row=0, column=0)
        title_label_2.grid(row=1, column=0)

        misc_setting_right = ctk.CTkButton(right_nav_frame,
                                           text="",
                                           image=self.ui_icons.get("settings"),
                                           width=20,
                                           height=20,
                                           font=ctk.CTkFont(size=20, weight="bold"), fg_color="transparent")
        misc_info_right = ctk.CTkButton(right_nav_frame,
                                        text="",
                                        image=self.ui_icons.get("info"),
                                        width=20,
                                        height=20,
                                        font=ctk.CTkFont(size=20, weight="bold"), fg_color="transparent")
        misc_setting_right.grid(row=0, column=0)
        misc_info_right.grid(row=0, column=1)

        self.orbital_gui = OrbitalMechanicsGUI(self)
        self.interplanetary_gui = InterplanetaryGUI(self)
        self.rocketry_gui = RocketryGUI(self)
        self.mission_planning_gui = MissionPlanningGUI(self)


        self.orbital_btn = ctk.CTkButton(center_nav_frame, text="Orbital Mechanics",
                                        command=self.orbital_gui.show_orbital_mechanics_frame,
                                        fg_color="transparent",
                                        hover_color="#16213E",
                                        font=ctk.CTkFont(size=16))
        self.mission_btn = ctk.CTkButton(center_nav_frame,
                                         text="Mission Planning",
                                         command=self.mission_planning_gui.show_mission_planning_frame,
                                         fg_color="transparent",
                                         hover_color="#16213E",
                                         font=ctk.CTkFont(size=16))
        self.rocketry_btn = ctk.CTkButton(center_nav_frame,
                                          text="Rocketry",
                                          command=self.rocketry_gui.show_rocketry_frame,
                                          fg_color="transparent",
                                          hover_color="#16213E",
                                          font=ctk.CTkFont(size=16))
        self.interplanetary_btn = ctk.CTkButton(center_nav_frame,
                                        text="Interplanetary Missions",
                                        command=self.interplanetary_gui.show_interplanetary_missions_frame,
                                        fg_color="transparent",
                                        hover_color="#16213E",
                                        font=ctk.CTkFont(size=16))
        self.orbital_btn.grid(row=0, column=0, sticky="nsew", padx=5)
        self.mission_btn.grid(row=0, column=1, sticky="nsew", padx=5)
        self.rocketry_btn.grid(row=0, column=2, sticky="nsew", padx=5)
        self.interplanetary_btn.grid(row=0, column=3, sticky="nsew", padx=5)

        self.nav_buttons = [
            self.orbital_btn,
            self.mission_btn,
            self.rocketry_btn,
            self.interplanetary_btn
        ]

        self.content_frame = ctk.CTkFrame(self, fg_color="#161616")
        self.content_frame.pack(fill="both", expand=True)

        # Initialize the GUI components
        self.orbital_gui.show_orbital_mechanics_frame()
        self.orbital_gui.update_body_information("Earth")

    def select_nav_button(self, selected_button):
        for button in self.nav_buttons:
            button.configure(
                fg_color="transparent"
            )

        selected_button.configure(
            fg_color="#1E40AF"
        )
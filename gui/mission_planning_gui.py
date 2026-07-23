import customtkinter as ctk
from data.dataloader import BODY_DATA


class MissionPlanningGUI:
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.logic = app.logic
        self.body_data = BODY_DATA

        self.mission_planning_master_frame = ctk.CTkFrame(self.app.content_frame, fg_color="transparent")


    def build_mission_planning_gui(self):
        self.mission_planning_master_frame = ctk.CTkFrame(self.app.content_frame, fg_color="transparent")

    def hide_gui(self):
        self.mission_planning_master_frame.grid_remove()

    def show_gui(self):
        self.mission_planning_master_frame.grid(row=0, column=0, sticky="nsew")

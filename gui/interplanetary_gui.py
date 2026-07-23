import customtkinter as ctk
class InterplanetaryGUI:
    def __init__(self, app):
        self.app = app
        self.interplanetary_master_frame = ctk.CTkFrame(self.app.content_frame, fg_color="transparent")


    def build_interplanetary_gui(self):
        self.interplanetary_master_frame = ctk.CTkFrame(self.app.content_frame, fg_color="transparent")

    def hide_gui(self):
        self.interplanetary_master_frame.grid_remove()

    def show_gui(self):
        self.interplanetary_master_frame.grid(row=0, column=0, sticky="nsew")
import customtkinter as ctk
from calculations.registry import CALCULATIONS
from PIL import Image
from assets.icons import PLANET_ICONS, UI_ICONS
from data.dataloader import BODY_DATA
from utils.helpers import resource_path
class OrbitalMechanicsGUI:
    """GUI class for Orbital Mechanics."""
    def __init__(self, app):
        super().__init__()
        self.logic = app.logic
        self.app = app
        self.body_data = BODY_DATA

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

    def build_orbital_gui(self):
        self.orbital_master_frame = ctk.CTkFrame(self.app.content_frame, fg_color="transparent")
        self.build_orbital_results_frame()
        self.build_orbital_input_frame()

    def hide_gui(self):
        self.orbital_master_frame.grid_remove()

    def show_gui(self):
        self.orbital_master_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

    def build_orbital_results_frame(self):
        # ------------------------------ ORBITAL RESULTS FRAME (RIGHT SIDE) ------------------------------
        self.results_frame = ctk.CTkFrame(self.orbital_master_frame,
                                          corner_radius=15,
                                          border_width=1,
                                          border_color="#2A2A2A",
                                          fg_color="#1C1C1C")
        self.results_frame.grid(row=0, column=1, padx=10, pady=20, sticky="nsew")
        self.results_frame.grid_columnconfigure(0, weight=1)
        # Title Frame
        title_frame = ctk.CTkFrame(self.results_frame, fg_color="transparent", corner_radius=10, height=50)
        title_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(10, 10))
        # RESULTS TITLE
        title_icon = ctk.CTkLabel(title_frame, text="", text_color="#3B82F6", font=ctk.CTkFont(size=18))

        title_text = ctk.CTkLabel(title_frame, text=" RESULTS", image=self.ui_icons.get("chart"), compound="left",
                                  font=ctk.CTkFont(size=20, weight="bold"))

        title_icon.pack(side="left", padx=(0, 5), pady=(0, 5))
        title_text.pack(side="left", padx=(0, 5), pady=(0, 5))

        # SEPARATOR

        separator1 = ctk.CTkFrame(self.results_frame, height=2, corner_radius=0, fg_color="#2A2A2A")
        separator1.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 10))
        separator1.grid_propagate(False)

        # MAIN RESULTS TITLE
        mission_title = ctk.CTkLabel(self.results_frame,
                                     text="MAIN RESULTS", font=ctk.CTkFont(size=18, weight="bold"),
                                     text_color="#60A5FA")

        mission_title.grid(row=2, column=0, sticky="w", padx=15, pady=(10, 10))

        # MAIN RESULTS CONTENTS
        self.main_results_frame = ctk.CTkFrame(self.results_frame,
                                               fg_color="transparent",
                                               height=120, width=900,
                                               corner_radius=20)
        self.main_results_frame.grid(row=3, column=0, padx=15, pady=(0, 10))
        self.main_results_frame.grid_columnconfigure(0, weight=1)
        self.main_results_frame.grid_propagate(False)

        self.result_calculation_label = ctk.CTkLabel(
            self.main_results_frame,
            text="",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#60A5FA")
        self.result_calculation_label.grid(row=0, column=0, padx=10, pady=(10, 0))

        self.main_result = ctk.CTkLabel(self.main_results_frame,
                                        text="Awaiting Calculation...",
                                        font=ctk.CTkFont(size=30),
                                        text_color="#1a8cf0")
        self.main_result.grid(row=1, column=0, padx=10, pady=10)

        self.secondary_result = ctk.CTkLabel(self.main_results_frame,
                                             text="",
                                             font=ctk.CTkFont(size=16),
                                             text_color="#505a63")
        self.secondary_result.grid(row=2, column=0, padx=10, pady=(0, 10))

        # SEPARATOR

        separator2 = ctk.CTkFrame(self.results_frame, height=2, corner_radius=0, fg_color="#2A2A2A")
        separator2.grid(row=4, column=0, sticky="ew", padx=15, pady=(0, 10))
        separator2.grid_propagate(False)

        # ADDITIONAL INFORMATION
        additional_info_title = ctk.CTkLabel(self.results_frame,
                                             text="ADDITIONAL INFORMATION",
                                             font=ctk.CTkFont(size=18, weight="bold"),
                                             text_color="#60A5FA")
        additional_info_title.grid(row=5, column=0, sticky="w", padx=15, pady=(10, 10))
        additional_info_frame = ctk.CTkFrame(self.results_frame,
                                             fg_color="transparent",
                                             height=190, width=600,
                                             corner_radius=20)
        additional_info_frame.grid(row=6, column=0, padx=15, sticky="ns")
        additional_info_frame.grid_columnconfigure(0, minsize=300)
        additional_info_frame.grid_columnconfigure(1, minsize=300)
        additional_info_frame.grid_rowconfigure(0, minsize=80)
        additional_info_frame.grid_rowconfigure(1, minsize=80)
        additional_info_frame.grid_propagate(False)
        self.info_card_1 = ctk.CTkFrame(additional_info_frame, fg_color="gray15", corner_radius=10)
        self.info_card_1.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        self.info_card_1.grid_propagate(False)
        self.info_card_1_title = ctk.CTkLabel(
            self.info_card_1,
            text="No data",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#a8a8a8")
        self.info_card_1_title.pack(side="top", padx=10, pady=(10, 0))
        self.info_card_1_value = ctk.CTkLabel(
            self.info_card_1,
            text="---",
            font=ctk.CTkFont(size=22),
            text_color="#FFFFFF")
        self.info_card_1_value.pack(side="top", padx=10, pady=(10, 10))

        self.info_card_2 = ctk.CTkFrame(additional_info_frame, fg_color="gray15", corner_radius=10)
        self.info_card_2.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        self.info_card_2.grid_propagate(False)
        self.info_card_2_title = ctk.CTkLabel(
            self.info_card_2,
            text="No data",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#a8a8a8")
        self.info_card_2_title.pack(side="top", padx=10, pady=(10, 0))
        self.info_card_2_value = ctk.CTkLabel(
            self.info_card_2,
            text="---",
            font=ctk.CTkFont(size=22),
            text_color="#FFFFFF")
        self.info_card_2_value.pack(side="top", padx=10, pady=(10, 10))

        self.info_card_3 = ctk.CTkFrame(additional_info_frame, fg_color="gray15", corner_radius=10)
        self.info_card_3.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.info_card_3.grid_propagate(False)
        self.info_card_3_title = ctk.CTkLabel(
            self.info_card_3,
            text="No Data",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#a8a8a8")
        self.info_card_3_title.pack(side="top", padx=10, pady=(10, 0))
        self.info_card_3_value = ctk.CTkLabel(
            self.info_card_3,
            text="---",
            font=ctk.CTkFont(size=22),
            text_color="#FFFFFF")
        self.info_card_3_value.pack(side="top", padx=10, pady=(10, 10))

        self.info_card_4 = ctk.CTkFrame(additional_info_frame, fg_color="gray15", corner_radius=10)
        self.info_card_4.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")
        self.info_card_4.grid_propagate(False)
        self.info_card_4_title = ctk.CTkLabel(
            self.info_card_4,
            text="No Data",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#a8a8a8")
        self.info_card_4_title.pack(side="top", padx=10, pady=(10, 0))
        self.info_card_4_value = ctk.CTkLabel(
            self.info_card_4,
            text="---",
            font=ctk.CTkFont(size=22),
            text_color="#FFFFFF")
        self.info_card_4_value.pack(side="top", padx=10, pady=(10, 10))

        # SEPARATOR

        separator3 = ctk.CTkFrame(self.results_frame, height=2, corner_radius=0, fg_color="#2A2A2A")
        separator3.grid(row=8, column=0, sticky="ew", padx=15, pady=(10, 10))
        separator3.grid_propagate(False)

        # NOTES AND ASSUMPTIONS
        self.notes_frame = ctk.CTkFrame(self.results_frame, fg_color="transparent", height=150, corner_radius=20)
        self.notes_frame.grid(row=9, column=0, padx=15, pady=(10, 10), sticky="ew")
        self.notes_frame.grid_propagate(False)
        notes_title = ctk.CTkLabel(self.notes_frame,
                                   text="NOTES AND ASSUMPTIONS",
                                   font=ctk.CTkFont(size=18, weight="bold"),
                                   text_color="#60A5FA")
        notes_title.grid(row=0, column=0, sticky="w", padx=15, pady=(0, 5))

        note_and_assumption_1 = ctk.CTkLabel(
            self.notes_frame,
            text="• Calculations are based on classical Newtonian astrodynamics",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#FFFFFF")
        note_and_assumption_2 = ctk.CTkLabel(
            self.notes_frame,
            text="• The selected celestial body is assumed to be perfectly spherical.",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#FFFFFF")
        note_and_assumption_3 = ctk.CTkLabel(
            self.notes_frame,
            text="• Atmospheric drag, J2 perturbations, and third-body effects are neglected.",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#FFFFFF")
        note_and_assumption_4 = ctk.CTkLabel(
            self.notes_frame,
            text="• Orbital altitudes are measured above the body's mean radius.",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#FFFFFF")
        note_and_assumption_1.grid(row=1, column=0, sticky="w", padx=15)
        note_and_assumption_2.grid(row=2, column=0, sticky="w", padx=15)
        note_and_assumption_3.grid(row=3, column=0, sticky="w", padx=15)
        note_and_assumption_4.grid(row=4, column=0, sticky="w", padx=15)

    def build_orbital_input_frame(self):
        # ------------------------------ ORBITAL INPUTS FRAME (LEFT SIDE) ------------------------------
        self.inputs_frame = ctk.CTkFrame(self.orbital_master_frame,
                                         corner_radius=15,
                                         border_width=1,
                                         border_color="#2A2A2A",
                                         fg_color="#1C1C1C")
        self.inputs_frame.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")
        self.inputs_frame.grid_columnconfigure(0, weight=1)
        # INPUTS TITLE

        title_frame = ctk.CTkFrame(self.inputs_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(10, 15))

        title_icon = ctk.CTkLabel(title_frame,
                                  text="☰",
                                  text_color="#3B82F6",
                                  font=ctk.CTkFont(size=18))

        title_text = ctk.CTkLabel(title_frame,
                                  text="INPUTS",
                                  font=ctk.CTkFont(size=20, weight="bold"))

        title_icon.pack(side="left", padx=(0, 5))
        title_text.pack(side="left")

        # SEPARATOR

        separator1 = ctk.CTkFrame(self.inputs_frame, height=2, corner_radius=0, fg_color="#2A2A2A")
        separator1.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 10))
        separator1.grid_propagate(False)

        # MISSION SETUP TITLE

        mission_title = ctk.CTkLabel(self.inputs_frame,
                                     text="MISSION SETUP",
                                     font=ctk.CTkFont(size=18, weight="bold"),
                                     text_color="#60A5FA")

        mission_title.grid(row=2, column=0, sticky="w", padx=15, pady=(10, 0))

        # MISSION SETUP CONTENTS

        mission_frame = ctk.CTkFrame(self.inputs_frame, fg_color="transparent")

        mission_frame.grid(row=3, column=0, sticky="ew", padx=15)

        mission_frame.grid_columnconfigure(0, weight=0)
        mission_frame.grid_columnconfigure(1, weight=0)
        mission_frame.grid_columnconfigure(2, weight=0)

        # Celestial Body Label

        ctk.CTkLabel(mission_frame,
                     text="Celestial Body:",
                     font=ctk.CTkFont(size=16)).grid(row=0, column=0, sticky="w",padx=(0, 20))

        # Celestial Body Dropdown

        self.celestial_body_var = ctk.StringVar(value="Earth")

        self.planet_icon_label = ctk.CTkLabel(
            mission_frame,
            text="",
            image=self.planet_icons["Earth"]
        )

        self.planet_icon_label.grid(row=0, column=1, padx=(0, 5))

        self.celestial_dropdown = ctk.CTkOptionMenu(
            mission_frame,
            values=[
                "Mercury", "Venus", "Earth", "Moon", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"
            ],
            variable=self.celestial_body_var,
            command=self.update_body_information
        )

        self.celestial_dropdown.grid(row=0, column=2, padx=(0, 5), sticky="w")
        # Planet information

        planet_info_frame = ctk.CTkFrame(mission_frame,
                                         width=200,
                                         height=85,
                                         fg_color="gray15",
                                         corner_radius=10)
        planet_info_frame.grid(row=0, column=3, padx=(5, 0), pady=(0, 10), sticky="w")
        planet_info_frame.grid_propagate(False)
        self.planet_info_label = ctk.CTkLabel(planet_info_frame,
                                              text="",
                                              justify="left",
                                              text_color="gray70")
        self.planet_info_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        # SEPARATOR

        separator2 = ctk.CTkFrame(self.inputs_frame,
                                  height=2,
                                  fg_color="#2A2A2A")
        separator2.grid(row=5, column=0, sticky="ew", padx=15, pady=(10, 10))
        separator2.grid_propagate(False)

        # CALCULATION TYPE
        calculation_type_title = ctk.CTkLabel(self.inputs_frame,
                                              text="CALCULATION TYPE",
                                              font=ctk.CTkFont(size=18, weight="bold"),
                                              text_color="#60A5FA")

        calculation_type_title.grid(row=6, column=0, sticky="w", padx=15, pady=(10, 0))
        calculation_type_frame = ctk.CTkFrame(self.inputs_frame, fg_color="transparent", height=50)
        calculation_type_frame.grid(row=7, column=0, sticky="ew", padx=15)

        # CALCULATION LABEL
        ctk.CTkLabel(calculation_type_frame,
                     text="Calculation",
                     font=ctk.CTkFont(size=16)).grid(row=0, column=0, sticky="w", padx=(0, 43), pady=10)

        # CALCULATION TYPE DROPDOWN
        self.calculation_type_var = ctk.StringVar(value="Circular Orbital Velocity")
        ctk.CTkOptionMenu(calculation_type_frame,
                          values=list(CALCULATIONS.keys()), variable=self.calculation_type_var,
                          command=self.update_input_parameters, width=250, height=50,
                          fg_color="gray25", dropdown_fg_color="gray25"
                          ).grid(row=0, column=1, padx=(0, 10), sticky="w")

        # Input Parameters
        self.input_parameters_frame = ctk.CTkFrame(self.inputs_frame,
                                                   height=160,
                                                   fg_color="transparent",
                                                   corner_radius=10)
        self.input_parameters_frame.grid(row=8, column=0, sticky="ew", padx=15, pady=(10, 10))
        self.input_parameters_frame.grid_columnconfigure(0, weight=1)
        self.input_parameters_frame.grid_columnconfigure(1, weight=2)

        # Text for the input panels (left side)
        ctk.CTkLabel(self.input_parameters_frame, text="Orbital Altitude (km)", font=ctk.CTkFont(size=16)
                     ).grid(row=0, column=0, sticky="w", padx=(0, 10), pady=5)
        ctk.CTkLabel(self.input_parameters_frame, text="Periapsis (km)", font=ctk.CTkFont(size=16)
                     ).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=5)
        ctk.CTkLabel(self.input_parameters_frame, text="Apoapsis (km)", font=ctk.CTkFont(size=16)
                     ).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=5)

        # Entry panels (right side)
        self.entry_orbital_altitude = ctk.CTkEntry(
            self.input_parameters_frame, placeholder_text="Enter Orbital Altitude (km)", width=200)
        self.entry_orbital_altitude.grid(row=0, column=1, sticky="w", padx=(0, 10), pady=5)
        self.entry_periapsis = ctk.CTkEntry(
            self.input_parameters_frame, placeholder_text="Enter Periapsis (km)", width=200)
        self.entry_periapsis.grid(row=1, column=1, sticky="w", padx=(0, 10), pady=5)
        self.entry_apoapsis = ctk.CTkEntry(
            self.input_parameters_frame, placeholder_text="Enter Apoapsis (km)", width=200)
        self.entry_apoapsis.grid(row=2, column=1, sticky="w", padx=(0, 10), pady=5)
        self.input_parameters_frame.grid_propagate(False)

        # Frame for the info frame (inside the input parameters frame)
        self.info_frame = ctk.CTkFrame(
            self.input_parameters_frame, fg_color="transparent", corner_radius=10, height=40, width=500)
        self.info_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=15, pady=10)
        self.info_frame.grid_propagate(False)

        # Another frame (inside the info_frame)

        self.info_container = ctk.CTkFrame(self.info_frame, fg_color="transparent")
        self.info_container.pack(anchor="w")
        # Icon info (the logo)

        self.info_icon = ctk.CTkLabel(self.info_container, text="ⓘ", text_color="#60A5FA")
        self.info_icon.pack(side="left", padx=(0, 5))
        # Text info
        self.info_text = ctk.CTkLabel(self.info_container, text="", anchor="w")
        self.info_text.pack(side="left")

        # Assign specified sizes for the input frames. (to avoid dynamic sizes)
        self.input_parameters_frame.grid_rowconfigure(0, minsize=40)
        self.input_parameters_frame.grid_rowconfigure(1, minsize=40)
        self.input_parameters_frame.grid_rowconfigure(2, minsize=40)
        self.input_parameters_frame.grid_rowconfigure(3, minsize=50)

        # Update the information, and the entry boxes.
        self.update_input_parameters(self.calculation_type_var.get())

        self.orbital_calculate_frame = ctk.CTkFrame(
            self.inputs_frame, fg_color="transparent", corner_radius=10, height=50, width=500)
        self.orbital_calculate_frame.grid(row=9, column=0, sticky="ew", padx=15, pady=(10, 10))
        self.orbital_calculate_frame.grid_columnconfigure(0, weight=1)
        self.orbital_calculate_frame.grid_columnconfigure(1, weight=1)

        # Calculate Button
        self.orbital_calculate_button = ctk.CTkButton(self.orbital_calculate_frame,
                                                      text=" CALCULATE", image=self.ui_icons.get("rocket"),
                                                      compound="left", height=50, width=150, corner_radius=10,
                                                      font=ctk.CTkFont(size=16, weight="bold"),
                                                      fg_color="#1E3A8A", hover_color="#2563EB",
                                                      command=self.calculate_to_logic)
        self.orbital_calculate_button.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        # Clear Button
        self.orbital_clear_button = ctk.CTkButton(self.orbital_calculate_frame,
                                                  text="  CLEAR", image=self.ui_icons.get("trash"),
                                                  compound="left", height=50, width=150, corner_radius=10,
                                                  font=ctk.CTkFont(size=18, weight="bold"), fg_color="gray20",
                                                  hover_color="gray30", command=self.clear_entries)

        self.orbital_clear_button.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        self.update_body_information("Earth")

    def calculate_to_logic(self):
        # For calculation and passing to Logic
        try:
            """Retrieve the selected calculation and its metadata from the
             CALCULATIONS registry. This registry acts as the single source
             of truth for all calculations in Project Astra."""
            selected = self.calculation_type_var.get()
            selected_calculation = CALCULATIONS[selected]

            # Retrieve the selected celestial body from the dropdown menu.
            selected_body = self.celestial_body_var.get()

            # Extract the function name and the required dynamic inputs for the selected calculation
            function_name = selected_calculation["function_name"]
            dynamic_inputs = selected_calculation["dynamic_inputs"]
            # Store all required inputs that will be passed to the logic function.
            input_values = {}

            """orbit_type is calculation metadata (e.g. circular or elliptical)
            and is automatically passed to the logic layer. It is NOT
            provided by the user."""

            if "orbit_type" in selected_calculation:
                input_values["orbit_type"] = selected_calculation["orbit_type"]

            for parameter in dynamic_inputs:
                if parameter == "orbital_altitude":
                    input_values["orbital_altitude"] = self.logic.validate_float_input(
                        self.entry_orbital_altitude.get(), "Orbital Altitude")

                elif parameter == "periapsis":
                    input_values["periapsis"] = self.logic.validate_float_input(
                        self.entry_periapsis.get(), "Periapsis")

                elif parameter == "apoapsis":
                    input_values["apoapsis"] = self.logic.validate_float_input(
                        self.entry_apoapsis.get(), "Apoapsis")

            # Dynamically retrieve the appropriate logic function and execute the calculation.
            function = getattr(self.logic, function_name)
            result = function(selected_body, **input_values)
            # Display the calculated result in the results panel.
            self.main_result.configure(text=f"{result['main_result']} {result['main_unit']}")
            self.secondary_result.configure(text=f"{result['secondary_result']} {result['secondary_unit']}")
            # Additional Information
            additional_info_function_name = selected_calculation["additional_information_function"]
            info_function = getattr(self.logic, additional_info_function_name)
            info_result = info_function(selected_body, **input_values)
            self.update_additional_information(info_result)

        # Display user-friendly error messages whenever invalid input
        except ValueError as e:
            self.main_result.configure(text=str(e))

    def clear_entries(self):
        # For clearing entries (connected to clear button)
        entries = [
            self.entry_orbital_altitude,
            self.entry_periapsis,
            self.entry_apoapsis]

        for entry in entries:
            if entry.cget("state") == "normal":
                entry.delete(0, "end")

        self.reset_orbital_results()

    def update_body_information(self, selected_body):
        # This function is for the dynamic planetary information at orbital mechanics tab.

        self.planet_info_label.configure(
            text=f"μ (GM): {self.body_data[selected_body]['mu']} km³/s²\n"
                 f"Radius: {self.body_data[selected_body]['mean_radius']} km\n"
                 f"Surface Gravity: {self.body_data[selected_body]['surface_gravity']} m/s²\n"
                 f"SOI: {self.body_data[selected_body]['sphere_of_influence']} km"
        )
        self.planet_icon_label.configure(
            image=self.app.planet_icons[selected_body])
        self.reset_orbital_results()
        self.main_result.configure(text="Awaiting Calculation...")

    def update_result_information(self, calculation_name):
        # Update the result information
        self.result_calculation_label.configure(
            text=calculation_name)

        self.main_result.configure(
            text="Awaiting Calculation...")

    def update_additional_information(self, information):
        # Change the additonal information (4 mini tabs) in the orbital mechanics.
        titles = [
            self.info_card_1_title,
            self.info_card_2_title,
            self.info_card_3_title,
            self.info_card_4_title
        ]

        values = [
            self.info_card_1_value,
            self.info_card_2_value,
            self.info_card_3_value,
            self.info_card_4_value,
        ]

        for i, (title, value) in enumerate(information):
            titles[i].configure(text=title)
            values[i].configure(text=value)

    def reset_orbital_results(self):
        self.entry_orbital_altitude.configure(placeholder_text="Enter Orbital Altitude")
        self.entry_apoapsis.configure(placeholder_text="Enter Apoapsis")
        self.entry_periapsis.configure(placeholder_text="Enter Periapsis")

        self.main_result.configure(text="Ready for New Calculation")

        self.secondary_result.configure(text="")

        self.info_card_1_title.configure(text="No data")
        self.info_card_1_value.configure(text="---")

        self.info_card_2_title.configure(text="No data")
        self.info_card_2_value.configure(text="---")

        self.info_card_3_title.configure(text="No data")
        self.info_card_3_value.configure(text="---")

        self.info_card_4_title.configure(text="No data")
        self.info_card_4_value.configure(text="---")

    def disable_entry(self, entry):
        # ----- Disable entry on the orbital mechanics tab depending on choice -----
        entry.configure(state="normal")
        entry.delete(0, "end")
        entry.insert(0, "---")
        entry.configure(state="disabled")

    def enable_entry(self, entry, placeholder):
        # ----- Enable entry on the orbital mechanics tab depending on choice -----
        entry.configure(state="normal")
        entry.delete(0, "end")
        entry.configure(placeholder_text=placeholder)

    def update_input_parameters(self, selected_calculation):
        # Update Input Parameters
        # Disable everything first
        self.disable_entry(self.entry_orbital_altitude)
        self.disable_entry(self.entry_periapsis)
        self.disable_entry(self.entry_apoapsis)
        calculation_name = selected_calculation

        selected_calculation = CALCULATIONS[selected_calculation]
        dynamic_inputs = selected_calculation["dynamic_inputs"]
        for parameter in dynamic_inputs:
            if parameter == "orbital_altitude":
                self.enable_entry(self.entry_orbital_altitude, "Enter Orbital Altitude")
            elif parameter == "periapsis":
                self.enable_entry(self.entry_periapsis, "Enter Periapsis")
            elif parameter == "apoapsis":
                self.enable_entry(self.entry_apoapsis, "Enter Apoapsis")
        self.info_text.configure(text=selected_calculation["description"])
        self.update_result_information(calculation_name)
        self.reset_orbital_results()
        self.main_result.configure(text="Awaiting Calculation...")

        def show_orbital_gui(self):
            self.orbital_master_frame.grid(row=0, column=0, sticky="nsew")

        def hide_orbital_gui(self):
            self.master_frame.grid_remove()



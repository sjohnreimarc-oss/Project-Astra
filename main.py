import customtkinter as ctk
import math
from constants import mu, mean_radius, surface_gravity, sphere_of_influence
from calculations import CALCULATIONS

class OrbitalVelocity:
    """Handles orbital velocity calculations and input validation.
    Uses gravitational parameters and mean radii from `constants.py`.
    """
    def __init__(self):
        self.mu = mu
        self.mean_radius = mean_radius

    def calculate_velocity(self, orbit_type, body, current_altitude, periapsis=None, apoapsis=None):
        """Calculate orbital velocity based on orbit type and parameters.
        orbit_type: str - 'circular' or 'elliptical'
        apoapsis: float - apoapsis altitude in km
        periapsis: float - periapsis altitude in km
        body: str - celestial body name (e.g., 'Earth', 'Moon')
        Returns: float - orbital velocity in km/s
        Raises: ValueError for invalid inputs
        """
        mu_val = self.mu[body]
        radius_val = self.mean_radius[body]

        if orbit_type == 'circular':
            # For circular orbits, apoapsis and periapsis are equal
            r = current_altitude + radius_val
            velocity = math.sqrt(mu_val / r)

        elif orbit_type == 'elliptical':
            # For elliptical orbits, use vis-viva equation
            r = current_altitude + radius_val
            r_a = apoapsis + radius_val
            r_p = periapsis + radius_val
            semi_major_axis = (r_a + r_p) / 2
            velocity = math.sqrt(mu_val * (2 / r - 1 / semi_major_axis))

        else:
            raise ValueError("Unknown orbit type")

        return round(velocity, 3)

class EscapeVelocity:
    """Handles escape velocity calculations and input validation.
    Uses gravitational parameters and mean radii from `constants.py`."""
    def __init__(self):
        self.mu = mu
        self.mean_radius = mean_radius

    def calculate_velocity(self, body, current_altitude):
        mu_val = self.mu[body]
        radius_val = self.mean_radius[body]

        velocity = math.sqrt(2 * mu_val / (radius_val + current_altitude))
        return round(velocity, 3)

class OrbitalPeriod:
    """Handles orbital period calculations by Kepler's third law and input validation."""
    def __init__(self):
        self.mu = mu
        self.mean_radius = mean_radius

    def calculate_circular_period(self, body, orbital_altitude):
        # Implementation for circular orbital period calculation
        mu_val = self.mu[body]
        radius_val = self.mean_radius[body]

        orbital_time = 2 * math.pi * math.sqrt((radius_val + orbital_altitude) ** 3 / mu_val)
        return round(orbital_time, 3)

    def calculate_elliptical_period(self, body, periapsis, apoapsis):
        """Implementation for elliptical orbital period calculation
                Calculate orbital period using Kepler's third law
                Returns:
                float - orbital
                period in seconds."""
        mu_val = self.mu[body]
        radius_val = self.mean_radius[body]

        # Calculate semi-major axis
        r_a = apoapsis + radius_val
        r_p = periapsis + radius_val
        semi_major_axis = (r_a + r_p) / 2



        orbital_time = 2 * math.pi * math.sqrt(semi_major_axis ** 3 / mu_val)
        return round(orbital_time, 3)

class Tsiolkovsky:
    """Handles the rocket equation with the rocket equation."""
    pass

class HohmannTransfer:
    """Handles the Hohmann Transfer equations for interplanetary transfers."""
    """NOTE TO SELF: DO THIS AS A MANAGER CLASS; NOT AN EQUATION CLASS. 
    CALL OTHER CLASSES FOR THE CALCULATIONS. """
    pass

class HyperbolicExcessVelocity:
    """Handles the hyperbolic excess velocity calculations."""
    pass

class InjectionVelocity:
    """Handles the injection velocity calculations."""
    pass



class ProjectAstraLogic:
    """Handles the project astra logic calculations."""

    def __init__(self):
        self.mu = mu
        self.mean_radius = mean_radius
        self.orbital_velocity = OrbitalVelocity()
        self.escape_velocity = EscapeVelocity()
        self.orbital_period = OrbitalPeriod()

        '''
        Placeholders
        self.tsiolkovsky = Tsiolkovsky()
        self.hohmann_transfer = HohmannTransfer()
        self.hyperbolic_excess_velocity = HyperbolicExcessVelocity()
        self.injection_velocity = InjectionVelocity()
        '''

    def _validate_body(self, body):
        if body not in self.mu:
            raise ValueError("Invalid celestial body")
        if body not in self.mean_radius:
            raise ValueError("Invalid celestial body")

    def validate_float_input(self, value, parameter_name):
        value = value.strip()
        if value == "":
            raise ValueError(f"{parameter_name} cannot be left blank.")
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"{parameter_name} must be a valid number.")

    def calculate_orbital_velocity(self, body, orbit_type, orbital_altitude, periapsis=None, apoapsis=None):
        self._validate_body(body)

        if orbital_altitude < 0:
            raise ValueError("Current altitude cannot be negative")

        if orbit_type == "elliptical":
            if apoapsis is None or periapsis is None:
                raise ValueError("For elliptical orbits, both apoapsis and periapsis must be specified")
            if apoapsis < 0 or periapsis < 0:
                raise ValueError("Apoapsis and periapsis cannot be negative")
            if periapsis > apoapsis:
                raise ValueError("Periapsis cannot be greater than apoapsis")
            if orbital_altitude < periapsis or orbital_altitude > apoapsis:
                raise ValueError("Current altitude is outside the bounds of the orbit")

            return self.orbital_velocity.calculate_velocity(orbit_type, body, orbital_altitude, periapsis, apoapsis)
        elif orbit_type == "circular":
            return self.orbital_velocity.calculate_velocity(orbit_type, body, orbital_altitude, periapsis, apoapsis)
        else:
            raise ValueError("Unknown orbit type")

    def calculate_escape_velocity(self, body, orbital_altitude):
        self._validate_body(body)

        if orbital_altitude < 0:
            raise ValueError("Current altitude cannot be negative")

        return self.escape_velocity.calculate_velocity(body, orbital_altitude)

    def calculate_orbital_period(self, body, orbit_type, orbital_altitude = None, periapsis=None, apoapsis=None):
        self._validate_body(body)
        if orbit_type == "circular":
            if orbital_altitude is None:
                raise ValueError("Orbital altitude cannot be None")
            if orbital_altitude < 0:
                raise ValueError("Orbital altitude cannot be negative")
            return self.orbital_period.calculate_circular_period(body, orbital_altitude)
        elif orbit_type == "elliptical":
            if apoapsis is None or periapsis is None:
                raise ValueError("For elliptical orbits, both apoapsis and periapsis must be specified")
            if apoapsis < 0 or periapsis < 0:
                raise ValueError("Apoapsis and periapsis cannot be negative")
            if periapsis > apoapsis:
                raise ValueError("Periapsis cannot be greater than apoapsis")
            return self.orbital_period.calculate_elliptical_period(body, periapsis, apoapsis)

        else:
            raise ValueError("Unknown orbit type")

    '''
    TEMPORARY PLACEHOLDERS: the parameters are not finalized.
    def calculate_tsiolkovsky(self, body):
        pass
    
    def calculate_hohmann_transfer(self, body):
        pass
    
    def calculate_hyperbolic_excess_velocity(self, body):
        pass
    
    def calculate_injection_velocity(self, body):
        pass
    '''


class ProjectAstraGUI(ctk.CTk):
    """GUI class for Project Astra."""
    def __init__(self):
        super().__init__()
        self.title("Project Astra")
        self.geometry("1500x800")
        ctk.set_appearance_mode("Dark")

        # Instantiate the Logic
        self.logic = ProjectAstraLogic()

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

        title_label_1 = ctk.CTkLabel(left_nav_frame, text="🚀 Project Astra", font=ctk.CTkFont(size=18, weight="bold"))
        title_label_2 = ctk.CTkLabel(left_nav_frame, text="Astrodynamics Toolkit", font=ctk.CTkFont(size=12))
        title_label_1.grid(row=0, column=0)
        title_label_2.grid(row=1, column=0)

        self.orbital_btn = ctk.CTkButton(center_nav_frame, text="Orbital Mechanics",
                                    command=self.show_orbital_mechanics_frame, fg_color="transparent", hover_color="#16213E", font=ctk.CTkFont(size=16))
        self.mission_btn = ctk.CTkButton(center_nav_frame, text="Mission Planning",
                                    command=self.show_mission_planning_frame, fg_color="transparent", hover_color="#16213E", font=ctk.CTkFont(size=16))
        self.rocketry_btn = ctk.CTkButton(center_nav_frame, text="Rocketry",
                                    command=self.show_rocketry_frame, fg_color="transparent", hover_color="#16213E", font=ctk.CTkFont(size=16))
        self.interplanetary_btn = ctk.CTkButton(center_nav_frame, text="Interplanetary Missions",
                                    command=self.show_interplanetary_missions_frame, fg_color="transparent", hover_color="#16213E", font=ctk.CTkFont(size=16))
        self.orbital_btn.grid(row=0, column=0, sticky="nsew", padx=5)
        self.mission_btn.grid(row=0, column=1, sticky="nsew", padx=5)
        self.rocketry_btn.grid(row=0, column=2, sticky="nsew", padx=5)
        self.interplanetary_btn.grid(row=0, column=3, sticky="nsew", padx=5)

        misc_setting_right = ctk.CTkButton(right_nav_frame, text="⚙", width=20, height=20, font=ctk.CTkFont(size=20, weight="bold"), fg_color="transparent")
        misc_info_right = ctk.CTkButton(right_nav_frame, text="ⓘ", width=20, height=20, font=ctk.CTkFont(size=20, weight="bold"), fg_color="transparent")
        misc_setting_right.grid(row=0, column=0)
        misc_info_right.grid(row=0, column=1)

        self.nav_buttons = [
            self.orbital_btn,
            self.mission_btn,
            self.rocketry_btn,
            self.interplanetary_btn
        ]

        self.content_frame = ctk.CTkFrame(self, fg_color="#161616")
        self.content_frame.pack(fill="both", expand=True)

        self.show_orbital_mechanics_frame()
        self.update_body_information("Earth")

    def select_nav_button(self, selected_button):
        for button in self.nav_buttons:
            button.configure(
                fg_color="transparent"
            )

        selected_button.configure(
            fg_color="#1E40AF"
        )

    # For calculation and passing to Logic
    def calculate_to_logic(self):
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
                        self.entry_orbital_altitude.get(),"Orbital Altitude")
                elif parameter == "periapsis":
                    input_values["periapsis"] = self.logic.validate_float_input(
                        self.entry_periapsis.get(), "Periapsis")
                elif parameter == "apoapsis":
                    input_values["apoapsis"] = self.logic.validate_float_input(
                        self.entry_apoapsis.get(), "Apoapsis")

            # Dynamically retrieve the appropriate logic function and execute the calculation.
            function = getattr(self.logic, function_name)
            result= function(selected_body, **input_values)

            # Display the calculated result in the results panel.
            self.results_label.configure(text=result)

        # Display user-friendly error messages whenever invalid input
        except ValueError as e:
            self.results_label.configure(text=str(e))

    # Update results panel
    def update_orbital_results(self, result):
        self.results_label.configure(text=f"Orbital Results: {result}")

    # For clearing entries (connected to clear button)
    def clear_entries(self):

        entries = [
            self.entry_orbital_altitude,
            self.entry_periapsis,
            self.entry_apoapsis]

        for entry in entries:
            if entry.cget("state") == "normal":
                entry.delete(0, "end")

    def show_orbital_mechanics_frame(self):
        self.select_nav_button(self.orbital_btn)
        # Configure the tab layout (Input panel : Results panel = 1 : 2)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=2)
        self.content_frame.grid_rowconfigure(0, weight=1)

        self.inputs_frame = ctk.CTkFrame(self.content_frame,
                corner_radius=15, border_width=1, border_color="#2A2A2A", fg_color="#1C1C1C")
        self.results_frame = ctk.CTkFrame(self.content_frame,
                corner_radius=15, border_width=1, border_color="#2A2A2A", fg_color="#1C1C1C")
        self.inputs_frame.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")
        self.results_frame.grid(row=0, column=1, padx=10, pady=20, sticky="nsew")

    # ------------------------------ INPUTS FRAME (LEFT SIDE) ------------------------------
        # Configure the inputs frame
        self.inputs_frame.grid_columnconfigure(0, weight=1)

        # INPUTS TITLE

        title_frame = ctk.CTkFrame(self.inputs_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(10, 15))

        title_icon = ctk.CTkLabel(title_frame, text="☰", text_color="#3B82F6", font=ctk.CTkFont(size=18))

        title_text = ctk.CTkLabel(title_frame, text="INPUTS", font=ctk.CTkFont(size=20, weight="bold"))

        title_icon.pack(side="left", padx=(0, 5))
        title_text.pack(side="left")

        # SEPARATOR

        separator1 = ctk.CTkFrame( self.inputs_frame, height=2, corner_radius=0, fg_color="#2A2A2A")
        separator1.grid( row=1, column=0, sticky="ew", padx=15, pady=(0, 10))
        separator1.grid_propagate(False)

        # MISSION SETUP TITLE

        mission_title = ctk.CTkLabel(self.inputs_frame,
                    text="MISSION SETUP", font=ctk.CTkFont(size=18, weight="bold"), text_color="#60A5FA")

        mission_title.grid(row=2, column=0, sticky="w", padx=15, pady=(10, 0))

        # MISSION SETUP CONTENTS

        mission_frame = ctk.CTkFrame(self.inputs_frame, fg_color="transparent")

        mission_frame.grid(row=3, column=0, sticky="ew", padx=15)

        mission_frame.grid_columnconfigure(0, weight=0)
        mission_frame.grid_columnconfigure(1, weight=0)
        mission_frame.grid_columnconfigure(2, weight=0)

        # Celestial Body Label

        ctk.CTkLabel(mission_frame, text="Celestial Body:", font=ctk.CTkFont(size=16)).grid(row=0, column=0, sticky="w", padx=(0,20))

        # Celestial Body Dropdown

        self.celestial_body_var = ctk.StringVar(value="Earth")

        ctk.CTkOptionMenu(mission_frame,
            values=[
                "Mercury",
                "Venus",
                "Earth",
                "Moon",
                "Mars",
                "Jupiter",
                "Saturn",
                "Uranus",
                "Neptune"], variable=self.celestial_body_var, width=180, height=50,
            fg_color="gray25", dropdown_fg_color="gray25", command=self.update_body_information).grid(row=0, column=1, padx=(0, 5), sticky="w")

        # Planet information

        planet_info_frame = ctk.CTkFrame(mission_frame, width=200, height=85, fg_color="gray15", corner_radius=10)
        planet_info_frame.grid(row=0, column=2, padx=(5, 0), pady=(0, 10), sticky="w")
        planet_info_frame.grid_propagate(False)
        self.planet_info_label = ctk.CTkLabel(planet_info_frame, text="", justify="left", text_color="gray70")
        self.planet_info_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        # SEPARATOR

        separator2 = ctk.CTkFrame(self.inputs_frame, height=2, fg_color="#2A2A2A")
        separator2.grid(row=5, column=0, sticky="ew", padx=15, pady=(10, 10))
        separator2.grid_propagate(False)

        # CALCULATION TYPE
        calculation_type_title = ctk.CTkLabel(self.inputs_frame,
                    text="CALCULATION TYPE", font=ctk.CTkFont(size=18, weight="bold"), text_color="#60A5FA")

        calculation_type_title.grid(row=6, column=0, sticky="w", padx=15, pady=(10, 0))
        calculation_type_frame = ctk.CTkFrame(self.inputs_frame, fg_color="transparent", height=50)
        calculation_type_frame.grid(row=7, column=0, sticky="ew", padx=15)

        # CALCULATION LABEL
        ctk.CTkLabel(calculation_type_frame, text="Calculation", font=ctk.CTkFont(size=16)).grid(row=0, column=0, sticky="w", padx=(0,43), pady=10)
        # CALCULATION TYPE DROPDOWN
        self.calculation_type_var = ctk.StringVar(value="Circular Orbital Velocity")
        ctk.CTkOptionMenu(calculation_type_frame,
            values=list(CALCULATIONS.keys()), variable=self.calculation_type_var, command=self.update_input_parameters, width=250, height=50,
            fg_color="gray25", dropdown_fg_color="gray25").grid(row=0, column=1, padx=(0, 10), sticky="w")

        # Input Parameters
        self.input_parameters_frame = ctk.CTkFrame(self.inputs_frame, height=160, fg_color="transparent", corner_radius=10)
        self.input_parameters_frame.grid(row=8, column=0, sticky="ew", padx=15, pady=(10, 10))
        self.input_parameters_frame.grid_columnconfigure(0, weight=1)
        self.input_parameters_frame.grid_columnconfigure(1, weight=2)

        # Text for the input panels (left side)
        ctk.CTkLabel(self.input_parameters_frame, text="Orbital Altitude (km)", font=ctk.CTkFont(size=16)
                     ).grid(row=0, column=0, sticky="w", padx=(0,10), pady=5)
        ctk.CTkLabel(self.input_parameters_frame, text="Periapsis (km)", font=ctk.CTkFont(size=16)
                     ).grid(row=1, column=0, sticky="w", padx=(0,10), pady=5)
        ctk.CTkLabel(self.input_parameters_frame, text="Apoapsis (km)", font=ctk.CTkFont(size=16)
                     ).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=5)

        # Entry panels (right side)
        self.entry_orbital_altitude = ctk.CTkEntry(self.input_parameters_frame, placeholder_text="Enter Orbital Altitude (km)", width=200)
        self.entry_orbital_altitude.grid(row=0, column=1, sticky="w", padx=(0, 10), pady=5)
        self.entry_periapsis = ctk.CTkEntry(self.input_parameters_frame, placeholder_text="Enter Periapsis (km)", width=200)
        self.entry_periapsis.grid(row=1, column=1, sticky="w", padx=(0, 10), pady=5)
        self.entry_apoapsis = ctk.CTkEntry(self.input_parameters_frame, placeholder_text="Enter Apoapsis (km)", width=200)
        self.entry_apoapsis.grid(row=2, column=1, sticky="w", padx=(0, 10), pady=5)
        self.input_parameters_frame.grid_propagate(False)

        # Frame for the info frame (inside the input parameters frame)
        self.info_frame = ctk.CTkFrame(self.input_parameters_frame, fg_color="transparent", corner_radius=10, height=40, width=500)
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

        self.orbital_calculate_frame = ctk.CTkFrame(self.inputs_frame, fg_color="transparent", corner_radius=10, height=50, width=500)
        self.orbital_calculate_frame.grid(row=9, column=0, sticky="ew", padx=15, pady=(10,10))
        self.orbital_calculate_frame.grid_columnconfigure(0, weight=1)
        self.orbital_calculate_frame.grid_columnconfigure(1, weight=1)

        # Calculate Button
        self.orbital_calculate_button = ctk.CTkButton(self.orbital_calculate_frame,
            text="🚀  CALCULATE", height=50, corner_radius=10, font=ctk.CTkFont(size=16,weight="bold"),
            fg_color="#1E3A8A", hover_color="#2563EB", command=self.calculate_to_logic)
        self.orbital_calculate_button.grid(row=0, column=0, sticky="ew", padx=(0,10))

        # Clear Button
        self.orbital_clear_button = ctk.CTkButton(
            self.orbital_calculate_frame, text="🗑  CLEAR", height=50, corner_radius=10,
            font=ctk.CTkFont(size=18, weight="bold"), fg_color="gray20",
            hover_color="gray30", command=self.clear_entries)

        self.orbital_clear_button.grid(row=0, column=1, sticky="ew", padx=(10, 0))

    # ------------------------------ RESULTS FRAME (RIGHT SIDE) ------------------------------
        self.results_label = ctk.CTkLabel(self.results_frame, text="Awaitin Calculation...", font=ctk.CTkFont(size=25,weight="bold"))
        self.results_label.grid(row=0, column=0, columnspan=2, sticky="ew")

    # This function is for the dynamic planetary information at orbital mechanics tab.
    def update_body_information(self, selected_body):
        mu_val = mu[selected_body]
        radius_val = mean_radius[selected_body]
        surface_gravity_val = surface_gravity[selected_body]
        soi_val = sphere_of_influence[selected_body]

        self.planet_info_label.configure(
            text=f"μ (GM): {mu_val} km³/s²\n"
             f"Radius: {radius_val} km\n"
             f"Surface Gravity: {surface_gravity_val} m/s²\n"
             f"SOI: {soi_val} km"
        )

    # ----- Disable/Enable entry on the orbital mechanics tab depending on choice -----
    def disable_entry(self, entry):
        entry.configure(state="normal")
        entry.delete(0, "end")
        entry.insert(0, "---")
        entry.configure(state="disabled")

    def enable_entry(self, entry, placeholder):
        entry.configure(state="normal")
        entry.delete(0, "end")
        entry.configure(placeholder_text=placeholder)

    # ----------------------------------------------------------------------------------
    # Update Input Parameters
    def update_input_parameters(self, selected_calculation):
        # Disable everything first
        self.disable_entry(self.entry_orbital_altitude)
        self.disable_entry(self.entry_periapsis)
        self.disable_entry(self.entry_apoapsis)

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

    def show_mission_planning_frame(self):
        self.select_nav_button(self.mission_btn)
        print("show_mission_planning_frame")

    def show_rocketry_frame(self):
        self.select_nav_button(self.rocketry_btn)
        print("show_rocketry_frame")

    def show_interplanetary_missions_frame(self):
        self.select_nav_button(self.interplanetary_btn)
        print("show_interplanetary_missions_frame")



if __name__ == "__main__":
    app = ProjectAstraGUI()
    app.mainloop()

import customtkinter as ctk
import math
from constants import mu, mean_radius, surface_gravity, sphere_of_influence
from calculations import CALCULATIONS
from PIL import Image
from icons import PLANET_ICONS, UI_ICONS

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

        return round(velocity, 3) # km/s

    def calculate_apoapsis_velocity(self, body, periapsis, apoapsis):
        mu_val = self.mu[body]
        radius_val = self.mean_radius[body]

        r_a = apoapsis + radius_val
        r_p = periapsis + radius_val
        semi_major_axis = (r_a + r_p) / 2

        velocity_apoapsis = math.sqrt(mu_val * (2 / r_a - 1 / semi_major_axis))
        return round(velocity_apoapsis, 3) # km/s

    def calculate_periapsis_velocity(self, body, periapsis, apoapsis):
        mu_val = self.mu[body]
        radius_val = self.mean_radius[body]

        r_a = apoapsis + radius_val
        r_p = periapsis + radius_val
        semi_major_axis = (r_a + r_p) / 2

        velocity_periapsis = math.sqrt(mu_val * (2 / r_p - 1 / semi_major_axis))
        return round(velocity_periapsis, 3) # km/s

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
        return round(velocity, 3) # km/s

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
        return round(orbital_time, 3) # seconds

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
        return round(orbital_time, 3) # seconds

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

class Eccentricity:
    """For calculating the eccentricity of an elliptical orbit."""
    def __init__(self):
        self.mean_radius = mean_radius
        self.utilities = Utilities()

    def calculate_eccentricity(self, body, periapsis, apoapsis):
        # Implementation for calculating eccentricity
        # Calculate the semi-major axis
        semi_major = self.utilities.calculate_semi_major(body, periapsis, apoapsis)
        rp = self.mean_radius[body] + periapsis
        ra = self.mean_radius[body] + apoapsis
        # Calculate the eccentricity
        eccentricity = (ra - rp) / (ra + rp)
        return round(eccentricity, 3)


class Utilities:
    """Calculate utilities such as seconds to days, km/s to km/h, orbital radius, etc."""
    def __init__(self):
        self.mu = mu
        self.mean_radius = mean_radius
        self.soi = sphere_of_influence

    def convert_seconds(self, seconds):
        """Convert seconds to a more readable format (days, hours, minutes, seconds)."""
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        seconds = round(seconds, 3)  # Round to 3 decimal places
        time_string = ""
        if days > 0:
            time_string += f"{int(days)} d, "
        if hours > 0:
            time_string += f"{int(hours)} h, "
        if minutes > 0:
            time_string += f"{int(minutes)} min, "
        time_string += f"{seconds}"
        return time_string

    def convert_kms_to_kmh(self, velocity_kms):
        """Convert velocity from km/s to km/h."""
        return round(velocity_kms * 3600, 3)

    def calculate_semi_major(self, body, periapsis, apoapsis):
        """Calculate the semi-major axis of the orbit."""
        radius = float(self.mean_radius[body])
        rp = radius + periapsis
        ra = radius + apoapsis
        semi_major = (rp + ra) / 2
        return round(semi_major, 3)

    def calculate_orbital_radius(self, body, orbital_height):
        """Calculate the orbital radius of the orbit."""
        radius = float(self.mean_radius[body])
        orbital_altitude = radius + orbital_height
        return round(orbital_altitude, 3)

    def calculate_orbital_circumference(self, body, orbital_height):
        """Calculate the orbital circumference with 2pi * r"""
        radius = float(self.mean_radius[body])
        orbital_circumference = 2 * math.pi * (radius + orbital_height)
        return round(orbital_circumference, 3)

    def calculate_velocity_ratio(self, escape_velocity, circular_velocity):
        """Calculate the ratio of escape velocity to circular orbital velocity."""
        if circular_velocity == 0:
            raise ValueError("Circular velocity cannot be zero for ratio calculation.")
        return round(escape_velocity / circular_velocity, 3)

    def calculate_local_gravity(self, body, orbital_height):
        """Calculate the local gravity of the celestial body."""
        mean_radius = float(self.mean_radius[body]) + orbital_height
        mu = float(self.mu[body])
        g = (mu / (mean_radius ** 2)) * 1000  # Convert to m/s^2
        return round(g, 3)

    def calculate_orbits_per_day(self, orbital_circumference, circular_velocity):
        """Calculate the number of orbits per day."""
        time_per_orbit = orbital_circumference / circular_velocity
        orbits_per_day = 86400 / time_per_orbit  # 86400 seconds in a day
        return round(orbits_per_day, 3)

    def calculate_apoapsis_radius(self, body, apoapsis):
        """Calculate the apoapsis radius of the orbit."""
        radius = float(self.mean_radius[body])
        apoapsis_radius = radius + apoapsis
        return round(apoapsis_radius, 3)

    def calculate_periapsis_radius(self, body, periapsis):
        """Calculate the periapsis radius of the orbit."""
        radius = float(self.mean_radius[body])
        periapsis_radius = radius + periapsis
        return round(periapsis_radius, 3)

class ProjectAstraLogic:
    """Handles the project astra logic calculations."""

    def __init__(self):
        self.mu = mu
        self.mean_radius = mean_radius
        self.surface_gravity = surface_gravity
        self.soi = sphere_of_influence
        self.orbital_velocity = OrbitalVelocity()
        self.escape_velocity = EscapeVelocity()
        self.orbital_period = OrbitalPeriod()
        self.eccentricity = Eccentricity()
        self.utilities = Utilities()

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

            velocity_kms = self.orbital_velocity.calculate_velocity(orbit_type, body, orbital_altitude, periapsis, apoapsis)
            # Convert km/s to km/h
            velocity_kmh = self.utilities.convert_kms_to_kmh(velocity_kms)
            return {"main_result": velocity_kms, "main_unit": "km/s", "secondary_result": velocity_kmh, "secondary_unit": "km/h"}
        elif orbit_type == "circular":
            velocity_kms = self.orbital_velocity.calculate_velocity(orbit_type, body, orbital_altitude, periapsis, apoapsis)
            # Convert km/s to km/h
            velocity_kmh = self.utilities.convert_kms_to_kmh(velocity_kms)
            return {"main_result": velocity_kms, "main_unit": "km/s", "secondary_result": velocity_kmh, "secondary_unit": "km/h"}

        else:
            raise ValueError("Unknown orbit type")

    def calculate_escape_velocity(self, body, orbital_altitude):
        self._validate_body(body)

        if orbital_altitude < 0:
            raise ValueError("Current altitude cannot be negative")
        velocity_kms = self.escape_velocity.calculate_velocity(body, orbital_altitude)
        # Convert km/s to km/h
        velocity_kmh = self.utilities.convert_kms_to_kmh(velocity_kms)
        return {"main_result": velocity_kms, "main_unit": "km/s", "secondary_result": velocity_kmh, "secondary_unit": "km/h"}

    def calculate_orbital_period(self, body, orbit_type, orbital_altitude = None, periapsis=None, apoapsis=None):
        self._validate_body(body)
        if orbit_type == "circular":
            if orbital_altitude is None:
                raise ValueError("Orbital altitude cannot be None")
            if orbital_altitude < 0:
                raise ValueError("Orbital altitude cannot be negative")
            result = self.orbital_period.calculate_circular_period(body, orbital_altitude)
            return {"main_result": self.utilities.convert_seconds(result), "main_unit": "seconds", "secondary_result": result, "secondary_unit": "s"}
        elif orbit_type == "elliptical":
            if apoapsis is None or periapsis is None:
                raise ValueError("For elliptical orbits, both apoapsis and periapsis must be specified")
            if apoapsis < 0 or periapsis < 0:
                raise ValueError("Apoapsis and periapsis cannot be negative")
            if periapsis > apoapsis:
                raise ValueError("Periapsis cannot be greater than apoapsis")
            result = self.orbital_period.calculate_elliptical_period(body, periapsis, apoapsis)
            return {"main_result": self.utilities.convert_seconds(result), "main_unit": "seconds", "secondary_result": result, "secondary_unit": "s"}

        else:
            raise ValueError("Unknown orbit type")

    def get_circular_velocity_information(self, body, orbital_altitude, **kwargs):
        self._validate_body(body)
        """ADDITIONAL INFO
        Circular Orbital Velocity
        - Orbital Radius
        - Escape Velocity
        - Orbital Period
        - Orbital Circumference"""
        # Card 1 - Orbital Radius
        orbital_radius = self.utilities.calculate_orbital_radius(body, orbital_altitude)
        escape_velocity = self.escape_velocity.calculate_velocity(body, orbital_altitude)
        orbital_period = self.orbital_period.calculate_circular_period(body, orbital_altitude)
        orbital_circumference = self.utilities.calculate_orbital_circumference(body, orbital_altitude)

        return [("Orbital Radius", f"{orbital_radius} km"),
                ("Escape Velocity", f"{escape_velocity} km/s"),
                ("Orbital Period", f"{self.utilities.convert_seconds(orbital_period)}"),
                ("Orbital Circumference", f"{orbital_circumference} km")]

    def get_elliptical_velocity_information(self, body, periapsis, apoapsis, **kwargs):
        self._validate_body(body)
        """ADDITIONAL INFO
        Elliptical Orbital Velocity
        - Semi-major Axis
        - Apoapsis Velocity
        - Periapsis Velocity
        - Eccentricity"""
        semi_major = self.utilities.calculate_semi_major(body, periapsis, apoapsis)
        apoapsis_vel = self.orbital_velocity.calculate_apoapsis_velocity(body, periapsis, apoapsis)
        periapsis_vel = self.orbital_velocity.calculate_periapsis_velocity(body, periapsis, apoapsis)
        eccentricity = self.eccentricity.calculate_eccentricity(body, periapsis, apoapsis)

        return [("Semi-major Axis", f"{semi_major} km"),
                ("Apoapsis Velocity", f"{apoapsis_vel} km/s"),
                ("Periapsis Velocity", f"{periapsis_vel} km/s"),
                ("Eccentricity", f"{eccentricity}")]

    def get_escape_velocity_information(self, body, orbital_altitude, **kwargs):
        self._validate_body(body)
        """ADDITIONAL INFO
        Escape Velocity
        - Surface Gravity
        - Orbital Radius
        - Circular Orbital Velocity
        - Velocity Ratio (Escape Velocity / Circular Orbital Velocity)"""
        local_gravity = self.utilities.calculate_local_gravity(body, orbital_altitude)
        orbital_radius = self.utilities.calculate_orbital_radius(body, orbital_altitude)
        circular_velocity = self.orbital_velocity.calculate_velocity("circular", body, orbital_altitude)
        escape_velocity = self.escape_velocity.calculate_velocity(body, orbital_altitude)
        velocity_ratio = self.utilities.calculate_velocity_ratio(escape_velocity, circular_velocity)
        return [
            ("Local Gravity", f"{local_gravity} m/s²"),
            ("Orbital Radius", f"{orbital_radius} km"),
            ("Circular Orbital Velocity", f"{circular_velocity} km/s"),
            ("Velocity Ratio", f"{velocity_ratio}")
        ]

    def get_circular_period_information(self, body, orbital_altitude, **kwargs):
        self._validate_body(body)
        """ADDITIONAL INFO
        Circular Orbital Period

        - Orbital Radius
        - Circular Orbit Radius
        - Circumference
        - Number of Orbits per Day"""
        local_gravity = self.utilities.calculate_local_gravity(body, orbital_altitude)
        circular_orbit_radius = self.utilities.calculate_orbital_radius(body, orbital_altitude)
        orbital_circumference = self.utilities.calculate_orbital_circumference(body, orbital_altitude)
        circular_velocity = self.orbital_velocity.calculate_velocity("circular", body, orbital_altitude)
        orbits_per_day = self.utilities.calculate_orbits_per_day(orbital_circumference, circular_velocity)

        return [
            ("Local Gravity", f"{local_gravity} m/s²"),
            ("Circular Orbit Radius", f"{circular_orbit_radius} km"),
            ("Orbital Circumference", f"{orbital_circumference} km"),
            ("Number of Orbits per Day", f"{orbits_per_day}")
        ]

    def get_elliptical_period_information(self, body, periapsis, apoapsis, **kwargs):
        self._validate_body(body)
        """ADDITIONAL INFO
        Elliptical Orbital Period
        - Semi-major Axis
        - Eccentricity
        - Apoapsis Radius
        - Periapsis Radius"""
        semi_major = self.utilities.calculate_semi_major(body, periapsis, apoapsis)
        eccentricity = self.eccentricity.calculate_eccentricity(body, periapsis, apoapsis)
        apoapsis_radius = self.utilities.calculate_apoapsis_radius(body, apoapsis)
        periapsis_radius = self.utilities.calculate_periapsis_radius(body, periapsis)
        return [
            ("Semi-major Axis", f"{semi_major} km"),
            ("Eccentricity", f"{eccentricity}"),
            ("Apoapsis Radius", f"{apoapsis_radius} km"),
            ("Periapsis Radius", f"{periapsis_radius} km")
        ]

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
        self.geometry("1500x850")
        ctk.set_appearance_mode("Dark")

        # Instantiate the Logic
        self.logic = ProjectAstraLogic()

        # Initialize the Icons
        self.planet_icons = {}
        for body, path in PLANET_ICONS.items():
            self.planet_icons[body] = ctk.CTkImage(
                light_image=Image.open(path),
                dark_image=Image.open(path),
                size=(25,25))

        self.ui_icons = {}
        for name, path in UI_ICONS.items():
            self.ui_icons[name] = ctk.CTkImage(
                light_image=Image.open(path),
                dark_image=Image.open(path),
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

        title_label_1 = ctk.CTkLabel(left_nav_frame, text=" Project Astra", image=self.ui_icons.get("rocket"), compound="left", font=ctk.CTkFont(size=18, weight="bold"))
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

        misc_setting_right = ctk.CTkButton(right_nav_frame, text="", image=self.ui_icons.get("settings"), width=20, height=20, font=ctk.CTkFont(size=20, weight="bold"), fg_color="transparent")
        misc_info_right = ctk.CTkButton(right_nav_frame, text="", image=self.ui_icons.get("info"), width=20, height=20, font=ctk.CTkFont(size=20, weight="bold"), fg_color="transparent")
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
        # Configure the inputs and results frame
        self.inputs_frame.grid_columnconfigure(0, weight=1)
        self.results_frame.grid_columnconfigure(0, weight=1)

        self.build_orbital_results_frame()
        self.build_orbital_input_frame()

    def build_orbital_input_frame(self):
        # ------------------------------ ORBITAL INPUTS FRAME (LEFT SIDE) ------------------------------
        # INPUTS TITLE

        title_frame = ctk.CTkFrame(self.inputs_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(10, 15))

        title_icon = ctk.CTkLabel(title_frame, text="☰", text_color="#3B82F6", font=ctk.CTkFont(size=18))

        title_text = ctk.CTkLabel(title_frame, text="INPUTS", font=ctk.CTkFont(size=20, weight="bold"))

        title_icon.pack(side="left", padx=(0, 5))
        title_text.pack(side="left")

        # SEPARATOR

        separator1 = ctk.CTkFrame(self.inputs_frame, height=2, corner_radius=0, fg_color="#2A2A2A")
        separator1.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 10))
        separator1.grid_propagate(False)

        # MISSION SETUP TITLE

        mission_title = ctk.CTkLabel(self.inputs_frame,
                                     text="MISSION SETUP", font=ctk.CTkFont(size=18, weight="bold"),
                                     text_color="#60A5FA")

        mission_title.grid(row=2, column=0, sticky="w", padx=15, pady=(10, 0))

        # MISSION SETUP CONTENTS

        mission_frame = ctk.CTkFrame(self.inputs_frame, fg_color="transparent")

        mission_frame.grid(row=3, column=0, sticky="ew", padx=15)

        mission_frame.grid_columnconfigure(0, weight=0)
        mission_frame.grid_columnconfigure(1, weight=0)
        mission_frame.grid_columnconfigure(2, weight=0)

        # Celestial Body Label

        ctk.CTkLabel(mission_frame, text="Celestial Body:", font=ctk.CTkFont(size=16)).grid(row=0, column=0, sticky="w",
                                                                                            padx=(0, 20))

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

        planet_info_frame = ctk.CTkFrame(mission_frame, width=200, height=85, fg_color="gray15", corner_radius=10)
        planet_info_frame.grid(row=0, column=3, padx=(5, 0), pady=(0, 10), sticky="w")
        planet_info_frame.grid_propagate(False)
        self.planet_info_label = ctk.CTkLabel(planet_info_frame, text="", justify="left", text_color="gray70")
        self.planet_info_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        # SEPARATOR

        separator2 = ctk.CTkFrame(self.inputs_frame, height=2, fg_color="#2A2A2A")
        separator2.grid(row=5, column=0, sticky="ew", padx=15, pady=(10, 10))
        separator2.grid_propagate(False)

        # CALCULATION TYPE
        calculation_type_title = ctk.CTkLabel(self.inputs_frame,
                                              text="CALCULATION TYPE", font=ctk.CTkFont(size=18, weight="bold"),
                                              text_color="#60A5FA")

        calculation_type_title.grid(row=6, column=0, sticky="w", padx=15, pady=(10, 0))
        calculation_type_frame = ctk.CTkFrame(self.inputs_frame, fg_color="transparent", height=50)
        calculation_type_frame.grid(row=7, column=0, sticky="ew", padx=15)

        # CALCULATION LABEL
        ctk.CTkLabel(calculation_type_frame, text="Calculation", font=ctk.CTkFont(size=16)).grid(row=0, column=0,
                                                                                                 sticky="w",
                                                                                                 padx=(0, 43), pady=10)
        # CALCULATION TYPE DROPDOWN
        self.calculation_type_var = ctk.StringVar(value="Circular Orbital Velocity")
        ctk.CTkOptionMenu(calculation_type_frame,
                          values=list(CALCULATIONS.keys()), variable=self.calculation_type_var,
                          command=self.update_input_parameters, width=250, height=50,
                          fg_color="gray25", dropdown_fg_color="gray25").grid(row=0, column=1, padx=(0, 10), sticky="w")

        # Input Parameters
        self.input_parameters_frame = ctk.CTkFrame(self.inputs_frame, height=160, fg_color="transparent",
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
        self.entry_orbital_altitude = ctk.CTkEntry(self.input_parameters_frame,
                                                   placeholder_text="Enter Orbital Altitude (km)", width=200)
        self.entry_orbital_altitude.grid(row=0, column=1, sticky="w", padx=(0, 10), pady=5)
        self.entry_periapsis = ctk.CTkEntry(self.input_parameters_frame, placeholder_text="Enter Periapsis (km)",
                                            width=200)
        self.entry_periapsis.grid(row=1, column=1, sticky="w", padx=(0, 10), pady=5)
        self.entry_apoapsis = ctk.CTkEntry(self.input_parameters_frame, placeholder_text="Enter Apoapsis (km)",
                                           width=200)
        self.entry_apoapsis.grid(row=2, column=1, sticky="w", padx=(0, 10), pady=5)
        self.input_parameters_frame.grid_propagate(False)

        # Frame for the info frame (inside the input parameters frame)
        self.info_frame = ctk.CTkFrame(self.input_parameters_frame, fg_color="transparent", corner_radius=10, height=40,
                                       width=500)
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

        self.orbital_calculate_frame = ctk.CTkFrame(self.inputs_frame, fg_color="transparent", corner_radius=10,
                                                    height=50, width=500)
        self.orbital_calculate_frame.grid(row=9, column=0, sticky="ew", padx=15, pady=(10, 10))
        self.orbital_calculate_frame.grid_columnconfigure(0, weight=1)
        self.orbital_calculate_frame.grid_columnconfigure(1, weight=1)

        # Calculate Button
        self.orbital_calculate_button = ctk.CTkButton(self.orbital_calculate_frame,
                                                      text=" CALCULATE", image=self.ui_icons.get("rocket"), compound="left", height=50, width=150, corner_radius=10,
                                                      font=ctk.CTkFont(size=16, weight="bold"),
                                                      fg_color="#1E3A8A", hover_color="#2563EB",
                                                      command=self.calculate_to_logic)
        self.orbital_calculate_button.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        # Clear Button
        self.orbital_clear_button = ctk.CTkButton(
            self.orbital_calculate_frame, text="  CLEAR", image=self.ui_icons.get("trash"), compound="left", height=50, width=150, corner_radius=10,
            font=ctk.CTkFont(size=18, weight="bold"), fg_color="gray20",
            hover_color="gray30", command=self.clear_entries)

        self.orbital_clear_button.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        self.update_body_information("Earth")

    def build_orbital_results_frame(self):
        # ------------------------------ ORBITAL RESULTS FRAME (RIGHT SIDE) ------------------------------
        # Title Frame
        title_frame = ctk.CTkFrame(self.results_frame, fg_color="transparent", corner_radius=10, height=50)
        title_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(10, 10))
        # RESULTS TITLE
        title_icon = ctk.CTkLabel(title_frame, text="", text_color="#3B82F6", font=ctk.CTkFont(size=18))

        title_text = ctk.CTkLabel(title_frame, text=" RESULTS", image=self.ui_icons.get("chart"), compound="left", font=ctk.CTkFont(size=20, weight="bold"))

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
        self.main_results_frame = ctk.CTkFrame(self.results_frame, fg_color="transparent", height=120, width=900, corner_radius=20)
        self.main_results_frame.grid(row=3, column=0, padx=15, pady=(0, 10))
        self.main_results_frame.grid_columnconfigure(0, weight=1)
        self.main_results_frame.grid_propagate(False)

        self.result_calculation_label = ctk.CTkLabel(self.main_results_frame, text="", font=ctk.CTkFont(size=16, weight="bold"), text_color="#60A5FA")
        self.result_calculation_label.grid(row=0, column=0, padx=10, pady=(10, 0))

        self.main_result = ctk.CTkLabel(self.main_results_frame, text="Awaiting Calculation...", font=ctk.CTkFont(size=30), text_color="#1a8cf0")
        self.main_result.grid(row=1, column=0, padx=10, pady=10)

        self.secondary_result = ctk.CTkLabel(self.main_results_frame, text="", font=ctk.CTkFont(size=16), text_color="#505a63")
        self.secondary_result.grid(row=2, column=0, padx=10, pady=(0, 10))

        # SEPARATOR

        separator2 = ctk.CTkFrame(self.results_frame, height=2, corner_radius=0, fg_color="#2A2A2A")
        separator2.grid(row=4, column=0, sticky="ew", padx=15, pady=(0, 10))
        separator2.grid_propagate(False)

        # ADDITIONAL INFORMATION
        additional_info_title = ctk.CTkLabel(self.results_frame,
                                     text="ADDITIONAL INFORMATION", font=ctk.CTkFont(size=18, weight="bold"),
                                     text_color="#60A5FA")
        additional_info_title.grid(row=5, column=0, sticky="w", padx=15, pady=(10, 10))
        additional_info_frame = ctk.CTkFrame(self.results_frame, fg_color="transparent", height=190, width=600, corner_radius=20)
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
        notes_title.grid(row=0, column=0, sticky="w", padx=15, pady=(0,5))

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

    def update_body_information(self, selected_body):
        # This function is for the dynamic planetary information at orbital mechanics tab.
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
        self.planet_icon_label.configure(
            image=self.planet_icons[selected_body])
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

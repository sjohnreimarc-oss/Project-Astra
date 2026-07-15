import customtkinter as ctk
import math
from constants import mu, mean_radius


class OrbitalVelocity:
    """Handles orbital velocity calculations and input validation.
    Uses gravitational parameters and mean radii from `constants.py`.
    """

    def __init__(self, body_defaults=None):
        # body_defaults is unused for now but keeps API flexible
        self.mu = mu
        self.radius = mean_radius

    def calculate(self, orbital_height, body="Earth"):
        """Calculate circular orbital velocity (km/s).
        orbital_height: str or number - height above surface in km
        body: string - key for constants (e.g. 'Earth', 'Moon')
        Returns: float velocity rounded to 3 decimals
        Raises: ValueError on invalid input
        Celestial Body defaults to 'Earth'
        """
        # Validate body
        if body not in self.mu or body not in self.radius:
            raise ValueError("Unknown celestial body")

        # Parse height
        try:
            h = float(orbital_height)
        except (TypeError, ValueError):
            raise ValueError("Invalid orbital height")

        # Use constants
        mu_val = float(self.mu[body])
        radius_val = float(self.radius[body])

        # Compute velocity: sqrt(mu / (radius + height))
        # Validate arithmetic domain (non-negative)
        denom = radius_val + h
        if denom <= 0:
            raise ValueError("Invalid orbital radius")

        vel = math.sqrt(mu_val / denom)
        return round(vel, 3)

class EscapeVelocity:
    """Handles escape velocity calculations and input validation.
    Uses gravitational parameters and mean radii from `constants.py`."""

    def __init__(self, body_defaults=None):
        self.mu = mu
        self.radius = mean_radius
        # Set up the constants

    def calculate(self, orbital_height, body="Earth"):
        """Calculate escape velocity (km/s).
        Defaults to Earth if no body is specified."""

        if body not in self.mu or body not in self.radius:
            raise ValueError("Unknown celestial body")
        try:
            h = float(orbital_height)
        except (TypeError, ValueError):
            raise ValueError("Invalid orbital height")

        mu_val = float(self.mu[body])
        radius_val = float(self.radius[body])
        denom = radius_val + h
        if denom <= 0:
            raise ValueError("Invalid orbital radius")
        esc_vel = math.sqrt(2 * mu_val / denom)
        return round(esc_vel, 3)

class OrbitalPeriod:
    """Handles orbital period calculations by Kepler's third law and input validation."""
    pass

class VisViva:
    """Handles the vis-viva equation for orbital velocity calculations."""
    pass

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


class ProjectAstraGUI(ctk.CTk):
    """GUI class for Project Astra."""

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")

        # Physics classes
        self.orbital = OrbitalVelocity()
        self.escape = EscapeVelocity()
        self.period = OrbitalPeriod()
        self.visviva = VisViva()
        self.rocket = Tsiolkovsky()
        self.hohmann = HohmannTransfer()
        self.injection = InjectionVelocity()

        # Reset Input for the Orbital Mechanics tab.
        self.value_entry = None

        # Window configuration
        self.title("Orbital Velocity Calculator V0.1")
        self.geometry("1680x900")

        # Create top navigation bar
        nav_bar = ctk.CTkFrame(self, height=55, corner_radius=0, fg_color="#1f2937")
        nav_bar.pack(side="top", fill="x")

        # System title label
        lbl_brand = ctk.CTkLabel(
            nav_bar,
            text="Project Astra - All-in-one orbital calculator",
            font=ctk.CTkFont(size=16, weight="bold"))
        lbl_brand.pack(side="left", padx=25, pady=12)

        # Create TabView container
        self.tab_view = ctk.CTkTabview(self, corner_radius=8)
        self.tab_view.pack(fill="both", expand=True, padx=15, pady=10)

        # Add application tabs
        self.tab_view.add("Orbital Mechanics")
        self.tab_view.add("Mission Planning")
        self.tab_view.add("Rocketry")
        self.tab_view.add("Interplanetary Missions")


        # Build each tab interface
        self.setup_orbital_mechanics_tab(self.tab_view.tab("Orbital Mechanics"))
        self.setup_mission_planning_tab(self.tab_view.tab("Mission Planning"))
        self.setup_rocketry_tab(self.tab_view.tab("Rocketry"))
        self.setup_interplanetary_mission_tab(self.tab_view.tab("Interplanetary Missions"))

    def setup_orbital_mechanics_tab(self, tab_name):

        # Configure the tab layout (Input panel : Results panel = 1 : 2)
        tab_name.grid_columnconfigure(0, weight=1)
        tab_name.grid_columnconfigure(1, weight=2)
        tab_name.grid_rowconfigure(0, weight=1)

        # Create the main input and results frames
        self.inputs_frame = ctk.CTkFrame(tab_name, corner_radius=15, fg_color="gray15")
        self.results_frame = ctk.CTkFrame(tab_name, corner_radius=15, fg_color="gray15")
        self.inputs_frame.grid(row=0, column=0, padx=30, pady=20, sticky="nsew")
        self.results_frame.grid(row=0, column=1, padx=30, pady=20, sticky="nsew")

        # Configure the frames to automatically resize with the window
        for frame in (self.inputs_frame, self.results_frame):
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_rowconfigure(0, weight=1)

        # Stores the selected orbital mechanics calculation
        self.calculation_type_var = ctk.StringVar(value="Orbital Velocity")

        # Create the container for all input widgets
        self.input_panel = ctk.CTkFrame(self.inputs_frame, fg_color="transparent")
        self.input_panel.grid(row=0, column=0, padx=20, pady=20)
        self.input_panel.grid_columnconfigure(0, weight=1)

        # Calculation type dropdown menu
        ctk.CTkLabel(self.input_panel, text="Calculation Type:",
                     font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, pady=(0, 10))

        ctk.CTkOptionMenu(
            self.input_panel,
            variable=self.calculation_type_var,
            values=["Orbital Velocity", "Escape Velocity", "Orbital Period", "Vis-viva Equation"],
            command=self.update_required_inputs,
        ).grid(row=1, column=0, pady=(0, 16), sticky="ew")

        # Celestial body dropdown menu
        ctk.CTkLabel(
            self.input_panel,
            text="Celestial Body:",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=2, column=0, pady=(0, 10))

        self.celestial_body_var = ctk.StringVar(value="Earth")

        ctk.CTkOptionMenu(
            self.input_panel,
            variable=self.celestial_body_var,
            values=[
                "Mercury",
                "Venus",
                "Earth",
                "Moon",
                "Mars",
                "Jupiter",
                "Saturn",
                "Uranus",
                "Neptune",
            ],
        ).grid(row=3, column=0, pady=(0, 16), sticky="ew")

        # Dynamic input widgets will be displayed here
        ctk.CTkLabel(self.input_panel, text="Required Inputs:",
                     font=ctk.CTkFont(size=16, weight="bold")).grid(row=4, column=0, pady=(0, 10))

        self.required_inputs_frame = ctk.CTkFrame(self.input_panel, fg_color="transparent")
        self.required_inputs_frame.grid(row=5, column=0, pady=(0, 18))

        # Button that performs the selected calculation
        self.calculate_button = ctk.CTkButton(
            self.input_panel,
            text="Calculate",
            height=44,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.calculate_selected,
        )
        self.calculate_button.grid(row=6, column=0, sticky="ew", pady=(8, 0))

        # Results panel setup
        self.result_panel = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        self.result_panel.grid(row=0, column=0, padx=24, pady=24, sticky="nsew")
        self.result_panel.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.result_panel, text="Results",
                     font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, pady=(0, 12))

        self.result_label = ctk.CTkLabel(self.result_panel, text="Result:",
                                         font=ctk.CTkFont(size=15))
        self.result_label.grid(row=1, column=0, pady=8)

        # Display the default required inputs (Orbital Velocity)
        self.update_required_inputs(self.calculation_type_var.get())

    def update_required_inputs(self, choice):

        # Remove the previous input widgets when changing calculations
        for widget in self.required_inputs_frame.winfo_children():
            widget.destroy()

        # Reset Vis-viva specific entry widgets
        self.r_entry = None
        self.a_entry = None

        # Single-input calculations
        if choice in ("Orbital Velocity", "Escape Velocity"):

            ctk.CTkLabel(self.required_inputs_frame,
                         text="Orbital Height (km)").grid(row=0, column=0, pady=(0, 6))

            self.value_entry = ctk.CTkEntry(self.required_inputs_frame, width=220)
            self.value_entry.grid(row=1, column=0)

        elif choice == "Orbital Period":

            ctk.CTkLabel(self.required_inputs_frame,
                         text="Value (km)").grid(row=0, column=0, pady=(0, 6))

            self.value_entry = ctk.CTkEntry(self.required_inputs_frame, width=220)
            self.value_entry.grid(row=1, column=0)

        # Two-input Vis-viva calculation
        elif choice == "Vis-viva Equation":

            ctk.CTkLabel(self.required_inputs_frame,
                         text="Orbital Radius r (km)").grid(row=0, column=0, pady=(0, 6))

            self.r_entry = ctk.CTkEntry(self.required_inputs_frame, width=220)
            self.r_entry.grid(row=1, column=0, pady=(0, 10))

            ctk.CTkLabel(self.required_inputs_frame,
                         text="Semi-major Axis a (km)").grid(row=2, column=0, pady=(0, 6))

            self.a_entry = ctk.CTkEntry(self.required_inputs_frame, width=220)
            self.a_entry.grid(row=3, column=0)

    def calculate_selected(self):
        # Get the selected calculation and celestial body
        choice = self.calculation_type_var.get()
        body = self.celestial_body_var.get()

        try:
            if choice == "Orbital Velocity":
                # single-input: orbital height
                result = self.orbital.calculate(self.value_entry.get(), body)
                display = f"{result} km/s"

            elif choice == "Escape Velocity":
                # single-input: orbital height
                result = self.escape.calculate(self.value_entry.get(), body)
                display = f"{result} km/s"

            elif choice == "Orbital Period":
                # single-input: value (implementation-specific)
                result = self.period.calculate(self.value_entry.get(), body)
                display = str(result)

            elif choice == "Vis-viva Equation":
                # two-inputs: r and a
                result = self.visviva.calculate(self.r_entry.get(), self.a_entry.get(), body)
                display = f"{result} km/s"

            else:
                display = "Invalid calculation type"

        except (ValueError, TypeError, AttributeError):
            # Any parsing / missing-widget / calculation error -> show Invalid input
            display = "Invalid input"

        # Show result in the right-side panel
        self.result_label.configure(text=display)

    def setup_mission_planning_tab(self, tab_name):
        pass

    def setup_rocketry_tab(self, tab_name):
        pass

    def setup_interplanetary_mission_tab(self, tab_name):
        pass


if __name__ == "__main__":
    app = ProjectAstraGUI()
    app.mainloop()

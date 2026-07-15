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

        # Window configuration
        self.title("Orbital Velocity Calculator V0.1")
        self.geometry("1680x900")

        # Physics classes
        self.orbital = OrbitalVelocity()
        self.escape = EscapeVelocity()
        self.period = OrbitalPeriod()
        self.visviva = VisViva()
        self.rocket = Tsiolkovsky()
        self.hohmann = HohmannTransfer()
        self.injection = InjectionVelocity()

        # Variables
        self.celestial_body_var = ctk.StringVar(value="Earth")
        self.orbital_height_var = ctk.StringVar(value="Orbital Height")

        # --------------------
        # GUI Widgets
        # --------------------

        # Orbital Height / Semi-major Axis Dropdown
        ctk.CTkLabel(self,text="Orbital Height (KM):").grid(row=0, column=0)
        self.input_type_dropdown = ctk.CTkOptionMenu(self,
            variable=self.orbital_height_var, values=["Orbital Height", "Semi-major Axis"])
        self.input_type_dropdown.grid(row=0, column=1, padx=10, pady=10)

        # Celestial Body Dropdown
        self.celestial_body_dropdown = ctk.CTkOptionMenu(self,
            variable=self.celestial_body_var,values=["Earth", "Moon"])
        self.celestial_body_dropdown.grid(row=1, column=0, padx=10, pady=10)

        # Buttons
        ctk.CTkButton(self, text="Calculate Orbital Velocity",
            command=self.calculate_orbital_velocity).grid(row=1, column=1)

        ctk.CTkButton(self,text="Calculate Escape Velocity",
            command=self.calculate_escape_velocity).grid(row=1, column=2)

        # Result Label
        self.result_label = ctk.CTkLabel(self,
            text="Result:")
        self.result_label.grid(row=2, column=0)

    # -----------------------------------------
    # Calculation Functions
    # -----------------------------------------

    def calculate_orbital_velocity(self):

        body = self.celestial_body_var.get()
        entry_text = self.entry_orbital_height.get()
        try:
            velocity = self.orbital.calculate(
                entry_text,
                body=body)
        except ValueError:
            self.result_label.configure(text="Invalid input")
            return

        self.result_label.configure(
            text=f"{velocity} km/s")

    def calculate_escape_velocity(self):
        body = self.celestial_body_var.get()
        entry_text = self.entry_orbital_height.get()
        try:
            velocity = self.escape.calculate(
                entry_text,
                body=body)

        except ValueError:
            self.result_label.configure(text="Invalid input")
            return

        self.result_label.configure(text=f"{velocity} km/s")
if __name__ == "__main__":
    app = ProjectAstraGUI()
    app.mainloop()

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


class ProjectAstraGUI:
    """GUI class for the Orbital Velocity Calculator using CustomTkinter."""

    def __init__(self):
        ctk.set_appearance_mode("dark")
        self.root = ctk.CTk()
        self.root.title("Orbital Velocity Calculator V0.1")
        self.root.geometry("500x500")

        self.orbital = OrbitalVelocity()

        # Widgets / state
        self.celestial_body_var = ctk.StringVar()
        self.celestial_body_var.set("Earth")

        ctk.CTkLabel(self.root, text="Orbital Height (KM): ").grid(row=0, column=0)
        self.entry_orbital_height = ctk.CTkEntry(self.root)
        self.entry_orbital_height.grid(row=0, column=1)

        #Dropdown menu for the celestial Bodies
        self.dropdown = ctk.CTkOptionMenu(
            self.root, variable=self.celestial_body_var, values=["Earth", "Moon"]
        )
        self.dropdown.grid(row=1, column=0, padx=10, pady=10)

        ctk.CTkButton(self.root, text="Calculate", command=self.calculate_orbital_velocity).grid(row=1, column=1)

        self.result_label = ctk.CTkLabel(self.root, text="Result:")
        self.result_label.grid(row=2, column=0)

    def calculate_orbital_velocity(self):
        body = self.celestial_body_var.get()
        entry_text = self.entry_orbital_height.get()
        try:
            velocity = self.orbital.calculate(entry_text, body=body)
        except ValueError:
            self.result_label.configure(text="Invalid input")
            return

        # Keep same formatting as original
        self.result_label.configure(text=str(velocity) + "km/s")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ProjectAstraGUI()
    app.run()

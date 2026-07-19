import math
from data.dataloader import BODY_DATA
class OrbitalVelocity:
    """Handles orbital velocity calculations and input validation.
    Uses gravitational parameters and mean radii from `constants.py`.
    """
    def __init__(self):
        self.mu = {body: data["mu"] for body, data in BODY_DATA.items()}
        self.mean_radius = {body: data["mean_radius"] for body, data in BODY_DATA.items()}

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
        self.mu = {body: data["mu"] for body, data in BODY_DATA.items()}
        self.mean_radius = {body: data["mean_radius"] for body, data in BODY_DATA.items()}

    def calculate_velocity(self, body, current_altitude):
        mu_val = self.mu[body]
        radius_val = self.mean_radius[body]

        velocity = math.sqrt(2 * mu_val / (radius_val + current_altitude))
        return round(velocity, 3) # km/s

class OrbitalPeriod:
    """Handles orbital period calculations by Kepler's third law and input validation."""
    def __init__(self):
        self.mu = {body: data["mu"] for body, data in BODY_DATA.items()}
        self.mean_radius = {body: data["mean_radius"] for body, data in BODY_DATA.items()}

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
        self.mu = {body: data["mu"] for body, data in BODY_DATA.items()}
        self.mean_radius = {body: data["mean_radius"] for body, data in BODY_DATA.items()}
        self.orbital_utilities = OrbitalUtilities()

    def calculate_eccentricity(self, body, periapsis, apoapsis):
        # Implementation for calculating eccentricity
        # Calculate the semi-major axis
        semi_major = self.orbital_utilities.calculate_semi_major(body, periapsis, apoapsis)
        rp = self.mean_radius[body] + periapsis
        ra = self.mean_radius[body] + apoapsis
        # Calculate the eccentricity
        eccentricity = (ra - rp) / (ra + rp)
        return round(eccentricity, 3)

class OrbitalUtilities:
    def __init__(self):
        self.mu = {body: data["mu"] for body, data in BODY_DATA.items()}
        self.mean_radius = {body: data["mean_radius"] for body, data in BODY_DATA.items()}
        self.soi = {body: data["sphere_of_influence"] for body, data in BODY_DATA.items()}

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

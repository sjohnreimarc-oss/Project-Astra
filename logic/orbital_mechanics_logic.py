from calculations.orbital_mechanics import OrbitalVelocity, EscapeVelocity, OrbitalPeriod, Eccentricity, OrbitalUtilities
from data.dataloader import BODY_DATA
from utils.conversions import convert_kms_to_kmh
from utils.formatters import convert_seconds

class OrbitalMechanicsLogic:
    """Handles the project astra logic calculations."""

    def __init__(self):
        self.mu = {body: data["mu"] for body, data in BODY_DATA.items()}
        self.mean_radius = {body: data["mean_radius"] for body, data in BODY_DATA.items()}
        self.surface_gravity = {body: data["surface_gravity"] for body, data in BODY_DATA.items()}
        self.soi = {body: data["sphere_of_influence"] for body, data in BODY_DATA.items()}
        self.orbital_velocity = OrbitalVelocity()
        self.escape_velocity = EscapeVelocity()
        self.orbital_period = OrbitalPeriod()
        self.eccentricity = Eccentricity()
        self.orbital_utilities = OrbitalUtilities()
        self.time = convert_seconds
        self.velocity = convert_kms_to_kmh

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

            velocity_kms = self.orbital_velocity.calculate_velocity(orbit_type, body, orbital_altitude, periapsis,
                                                                    apoapsis)
            # Convert km/s to km/h
            velocity_kmh = self.velocity(velocity_kms)
            return {"main_result": velocity_kms, "main_unit": "km/s", "secondary_result": velocity_kmh,
                    "secondary_unit": "km/h"}
        elif orbit_type == "circular":
            velocity_kms = self.orbital_velocity.calculate_velocity(orbit_type, body, orbital_altitude, periapsis,
                                                                    apoapsis)
            # Convert km/s to km/h
            velocity_kmh = self.velocity(velocity_kms)
            return {"main_result": velocity_kms, "main_unit": "km/s", "secondary_result": velocity_kmh,
                    "secondary_unit": "km/h"}

        else:
            raise ValueError("Unknown orbit type")

    def calculate_escape_velocity(self, body, orbital_altitude):
        self._validate_body(body)

        if orbital_altitude < 0:
            raise ValueError("Current altitude cannot be negative")
        velocity_kms = self.escape_velocity.calculate_velocity(body, orbital_altitude)
        # Convert km/s to km/h
        velocity_kmh = self.velocity(velocity_kms)
        return {"main_result": velocity_kms, "main_unit": "km/s", "secondary_result": velocity_kmh,
                "secondary_unit": "km/h"}

    def calculate_orbital_period(self, body, orbit_type, orbital_altitude=None, periapsis=None, apoapsis=None):
        self._validate_body(body)
        if orbit_type == "circular":
            if orbital_altitude is None:
                raise ValueError("Orbital altitude cannot be None")
            if orbital_altitude < 0:
                raise ValueError("Orbital altitude cannot be negative")
            result = self.orbital_period.calculate_circular_period(body, orbital_altitude)
            return {"main_result": self.time(result), "main_unit": "seconds", "secondary_result": result,
                    "secondary_unit": "s"}
        elif orbit_type == "elliptical":
            if apoapsis is None or periapsis is None:
                raise ValueError("For elliptical orbits, both apoapsis and periapsis must be specified")
            if apoapsis < 0 or periapsis < 0:
                raise ValueError("Apoapsis and periapsis cannot be negative")
            if periapsis > apoapsis:
                raise ValueError("Periapsis cannot be greater than apoapsis")
            result = self.orbital_period.calculate_elliptical_period(body, periapsis, apoapsis)
            return {"main_result": self.time(result), "main_unit": "seconds", "secondary_result": result,
                    "secondary_unit": "s"}

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
        orbital_radius = self.orbital_utilities.calculate_orbital_radius(body, orbital_altitude)
        escape_velocity = self.escape_velocity.calculate_velocity(body, orbital_altitude)
        orbital_period = self.orbital_period.calculate_circular_period(body, orbital_altitude)
        orbital_circumference = self.orbital_utilities.calculate_orbital_circumference(body, orbital_altitude)

        return [("Orbital Radius", f"{orbital_radius} km"),
                ("Escape Velocity", f"{escape_velocity} km/s"),
                ("Orbital Period", f"{self.time(orbital_period)}"),
                ("Orbital Circumference", f"{orbital_circumference} km")]

    def get_elliptical_velocity_information(self, body, periapsis, apoapsis, **kwargs):
        self._validate_body(body)
        """ADDITIONAL INFO
        Elliptical Orbital Velocity
        - Semi-major Axis
        - Apoapsis Velocity
        - Periapsis Velocity
        - Eccentricity"""
        semi_major = self.orbital_utilities.calculate_semi_major(body, periapsis, apoapsis)
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
        local_gravity = self.orbital_utilities.calculate_local_gravity(body, orbital_altitude)
        orbital_radius = self.orbital_utilities.calculate_orbital_radius(body, orbital_altitude)
        circular_velocity = self.orbital_velocity.calculate_velocity("circular", body, orbital_altitude)
        escape_velocity = self.escape_velocity.calculate_velocity(body, orbital_altitude)
        velocity_ratio = self.orbital_utilities.calculate_velocity_ratio(escape_velocity, circular_velocity)
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
        local_gravity = self.orbital_utilities.calculate_local_gravity(body, orbital_altitude)
        circular_orbit_radius = self.orbital_utilities.calculate_orbital_radius(body, orbital_altitude)
        orbital_circumference = self.orbital_utilities.calculate_orbital_circumference(body, orbital_altitude)
        circular_velocity = self.orbital_velocity.calculate_velocity("circular", body, orbital_altitude)
        orbits_per_day = self.orbital_utilities.calculate_orbits_per_day(orbital_circumference, circular_velocity)

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
        semi_major = self.orbital_utilities.calculate_semi_major(body, periapsis, apoapsis)
        eccentricity = self.eccentricity.calculate_eccentricity(body, periapsis, apoapsis)
        apoapsis_radius = self.orbital_utilities.calculate_apoapsis_radius(body, apoapsis)
        periapsis_radius = self.orbital_utilities.calculate_periapsis_radius(body, periapsis)
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


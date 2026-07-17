CALCULATIONS = {
    "Circular Orbital Velocity": {"orbit_type": "circular", "dynamic_inputs": ["orbital_altitude"],"function_name": "calculate_orbital_velocity", "description": "For Circular Orbital Velocity, only the Orbital Altitude is required."},
    "Elliptical Orbital Velocity": {"orbit_type": "elliptical","dynamic_inputs": ["orbital_altitude", "periapsis", "apoapsis"],"function_name": "calculate_orbital_velocity", "description": "For Elliptical Velocities, you need all of Periapsis, Apoapsis, and Orbital Altitude."},
    "Escape Velocity": {"dynamic_inputs": ["orbital_altitude"], "function_name": "calculate_escape_velocity", "description": "For Escape Velocity, only the orbital altitude is required."},
    "Circular Orbital Period": {"orbit_type": "circular", "dynamic_inputs": ["orbital_altitude"], "function_name": "calculate_orbital_period", "description": "For Circular Orbital Period, you only need the orbital altitude."},
    "Elliptical Orbital Period": {"orbit_type": "elliptical", "dynamic_inputs": ["periapsis", "apoapsis"], "function_name": "calculate_orbital_period", "description": "For Elliptical Orbital Period, you need the Periapsis and Apoapsis of your orbit."}}



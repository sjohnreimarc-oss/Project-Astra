CALCULATIONS = {

    "Circular Orbital Velocity": {
        "orbit_type": "circular",
        "dynamic_inputs": ["orbital_altitude"],
        "function_name": "calculate_orbital_velocity",
        "additional_information_function": "get_circular_velocity_information",
        "description": "For Circular Orbital Velocity, only the Orbital Altitude is required."
    },

    "Elliptical Orbital Velocity": {
        "orbit_type": "elliptical",
        "dynamic_inputs": ["orbital_altitude", "periapsis", "apoapsis"],
        "function_name": "calculate_orbital_velocity",
        "additional_information_function": "get_elliptical_velocity_information",
        "description": "For Elliptical Velocities, you need all of Periapsis, Apoapsis, and Orbital Altitude."
    },

    "Escape Velocity": {
        "dynamic_inputs": ["orbital_altitude"],
        "function_name": "calculate_escape_velocity",
        "additional_information_function": "get_escape_velocity_information",
        "description": "For Escape Velocity, only the orbital altitude is required."
    },

    "Circular Orbital Period": {
        "orbit_type": "circular",
        "dynamic_inputs": ["orbital_altitude"],
        "function_name": "calculate_orbital_period",
        "additional_information_function": "get_circular_period_information",
        "description": "For Circular Orbital Period, you only need the orbital altitude."
    },

    "Elliptical Orbital Period": {
        "orbit_type": "elliptical",
        "dynamic_inputs": ["periapsis", "apoapsis"],
        "function_name": "calculate_orbital_period",
        "additional_information_function": "get_elliptical_period_information",
        "description": "For Elliptical Orbital Period, you need the Periapsis and Apoapsis of your orbit."
    }

}
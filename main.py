import customtkinter as ctk
import math

root = ctk.CTk()
ctk.set_appearance_mode("dark")
root.title("Orbital Velocity Calculator V0.1")
root.geometry("500x500")

celestial_body_var = ctk.StringVar()
celestial_body_var.set("Earth")


mu_Earth = float(398600)
mu_Moon = float(4902.8)
radius_Earth = float(6371.8)
radius_Moon = float(1731.4)
def calculate_orbital_velocity():
    celestial_body = celestial_body_var.get()
    if celestial_body == "Earth":
        mu = mu_Earth
        radius = radius_Earth
    elif celestial_body == "Moon":
        mu = mu_Moon
        radius = radius_Moon
    try:
        orbital_radius = float(entry_orbital_height.get())
    except ValueError:
        result_label.configure(text="Invalid input")
        return
    try:
        circular_orbit_velocity = round(math.sqrt(mu/(orbital_radius+radius)),3)
    except ValueError:
        result_label.configure(text="Invalid input")
        return
    result_label.configure(text=str(circular_orbit_velocity) + "km/s")

ctk.CTkLabel(root, text="Orbital Height (KM): ").grid(row=0, column=0)
entry_orbital_height = ctk.CTkEntry(root)
entry_orbital_height.grid(row=0, column=1)

dropdown = ctk.CTkOptionMenu(root, variable=celestial_body_var, values=["Earth", "Moon"])
dropdown.grid(row=1, column=0, padx=10, pady=10)

ctk.CTkButton(root, text="Calculate", command=calculate_orbital_velocity).grid(row=1, column=1)
result_label = ctk.CTkLabel(root, text="Result:")
result_label.grid(row=2, column=0)

root.mainloop()

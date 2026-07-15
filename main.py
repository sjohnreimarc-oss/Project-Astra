from tkinter import *
from tkinter.messagebox import *
import math

root = Tk()
root.title("Orbital Velocity Calculator V0.1")
root.geometry("500x500")

celestial_body_var = StringVar()
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
    orbital_radius = float(entry_orbital_height.get())
    circular_orbit_velocity = round(math.sqrt(mu/(orbital_radius+radius)),3)
    result_label.config(text=str(circular_orbit_velocity) + "km/s")

Label(root, text="Orbital Height (KM): ").grid(row=0, column=0)
entry_orbital_height = Entry(root)
entry_orbital_height.grid(row=0, column=1)

dropdown = OptionMenu(root, celestial_body_var, "Earth", "Moon")

dropdown.grid(row=1, column=0, padx=10, pady=10)

Button(root, text="Calculate", command=calculate_orbital_velocity).grid(row=1, column=1)
result_label = Label(root, text="Result:")
result_label.grid(row=2, column=0)

root.mainloop()

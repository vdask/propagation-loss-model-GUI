import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import webbrowser

def open_pdf():
    webbrowser.open("5_Propagation_1_HMMY_STR.pdf")

class PropagationModelGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Propagation Model Calculator")
        
        self.frequency = tk.DoubleVar(value=150)  # MHz
        self.distance = tk.DoubleVar(value=1)     # km
        self.height_transmitter = tk.DoubleVar(value=50)  # meters
        self.height_receiver = tk.DoubleVar(value=30)     # meters

        # Dropdown list
        self.model_var = tk.StringVar(value="Okumura")
        self.area_var = tk.StringVar(value="Urban")
        self.model_options = ["Okumura", "Hata", "Free Space", "CCIR"]
        self.model_area = [" Urban", "Suburban", "Rural"]
        self.model_frame = ttk.LabelFrame(root, text="Propagation Model")
        self.model_frame.pack(pady=10, padx=10, side="left", expand='True', fill='both')
        self.area_frame = ttk.LabelFrame(root, text="Area:")
        self.area_frame.pack(pady=10, padx=10, side="bottom", expand='True', fill='both')
        ttk.Label(self.model_frame, text="Select Model:").pack(side="left", padx=5)
        ttk.Label(self.area_frame, text="Hata Area:").pack(side="left", padx=5)
        self.model_combobox = ttk.Combobox(self.model_frame, textvariable=self.model_var, values=self.model_options, state="readonly")
        self.model_combobox.pack(side="left")
        self.model_combobox.bind("<<ComboboxSelected>>", self.on_model_selected)
        self.model_combobox_area = ttk.Combobox(self.area_frame, textvariable=self.area_var, values=self.model_area, state="readonly")
        self.model_combobox_area.pack(side="left")
        self.model_combobox_area.config(state="disable")

        self.plot_frame = ttk.LabelFrame(root, text="Loss Graph")
        self.plot_frame.pack(pady=10,padx=10,side='right',expand='True', fill='both')
        self.param_frame = ttk.LabelFrame(root, text="Parameters")
        self.param_frame.pack(pady=10, padx=10, side="bottom", expand='True', fill='both')
        tk.Label(self.param_frame, text="Frequency (MHz):").grid(row=0, column=0, sticky="w")
        self.freq_entry = ttk.Entry(self.param_frame, textvariable=self.frequency)
        self.freq_entry.grid(row=0, column=1)
        tk.Label(self.param_frame, text="Distance (km):").grid(row=1, column=0, sticky="w")
        self.dist_entry = ttk.Entry(self.param_frame, textvariable=self.distance)
        self.dist_entry.grid(row=1, column=1)
        tk.Label(self.param_frame, text="Transmitter Height (m):").grid(row=2, column=0, sticky="w")
        self.ht_entry = ttk.Entry(self.param_frame, textvariable=self.height_transmitter)
        self.ht_entry.grid(row=2, column=1)
        tk.Label(self.param_frame, text="Receiver Height (m):").grid(row=3, column=0, sticky="w")
        self.hr_entry = ttk.Entry(self.param_frame, textvariable=self.height_receiver)
        self.hr_entry.grid(row=3, column=1)

        # Calculate button
        ttk.Button(self.param_frame, text="Calculate", command=self.calculate).grid(row=4, column=0, sticky="w")

        # Menu bar
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)
        
        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open PDF", command=open_pdf)
        self.menu_bar.add_cascade(label="Help", menu=self.file_menu)

        # equation of propagation models
        self.equation_frame = ttk.LabelFrame(root, text="Equation")
        self.equation_frame.pack(pady=10, padx=10, side="bottom", expand='True', fill='both')
        self.equation_label = tk.Label(self.equation_frame, text="", justify="center", wraplength=300)
        self.equation_label.pack(pady=10)

        # power loss of the receiver
        self.power_loss_frame = ttk.LabelFrame(root, text="Power Loss")
        self.power_loss_frame.pack(pady=10, padx=10, side="bottom", expand='True', fill='both')
        self.power_loss_label = tk.Label(self.power_loss_frame, text="", justify="right", wraplength=300, foreground='red')
        self.power_loss_label.pack(pady=10)

        self.pdf_frame = tk.Frame(root)
        self.pdf_frame.pack(pady=10, padx=10, side="left", expand='True', fill="both")
        
        # Info menu
        self.info_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.info_menu.add_command(label="Info", command=self.show_info)
        self.menu_bar.add_cascade(label="Info", menu=self.info_menu)

    def show_info(self):
        messagebox.showinfo("About", "Advanced Topics in Antennas, Propagation of EMF fields, and Wireless Networks.\n\nCreated by \n - Vardis Daskalakis, MTH295 and \n - Charilaos Koutsourelakis, MTP323")

    def on_model_selected(self, event):
        selected_model = self.model_var.get()
        if selected_model == "Free Space":
            self.ht_entry.config(state="disabled")
            self.hr_entry.config(state ="disabled")
        else:
            self.ht_entry.config(state="normal")
            self.hr_entry.config(state="normal")
        if selected_model == "Hata":
            self.model_combobox_area.config(state="enable")
            selected_area = self.area_var.get()    
        else:
            self.model_combobox_area.config(state="disable")

    def validate_frequency(self):
        freq = self.frequency.get()
        if freq > 3000:
            messagebox.showwarning("Warning", "Frequency value should not exceed 3000 MHz.")
        elif freq < 150:
            messagebox.showerror("Warning", "Frequency value should be between 150MHz and 1920MHz")
            return

    def validate_distance(self):
        dist = self.distance.get()
        if dist < 1 or dist > 100:
            messagebox.showerror("Error", "Distance value should be between 1 and 100 km.")
            self.dist_entry.delete(0, tk.END)
            self.dist_entry.insert(0, 1)  # Reset to default value
            return

    def validate_height(self, height_var, label):
        height = height_var.get()
        if height < 30 or height > 1000:
            messagebox.showerror("Error", f"{label} value should be between 30 and 1000 meters.")
            height_var.set(50)  # Reset to default value
            return 

    def calculate(self):
        self.validate_frequency()
        self.validate_distance()
        self.validate_height(self.height_transmitter, "Transmitter Height")
        self.validate_height(self.height_receiver, "Receiver Height")

        freq = self.frequency.get()
        dist = self.distance.get()
        dist = np.linspace(1, dist)  # Sample distances from 1 to 100 km
       
        h_t = self.height_transmitter.get()
        h_r = self.height_receiver.get()
        model = self.model_var.get()
        area = self.area_var.get()

        # Calculate propagation loss based on selected model
        equation_text = ""
        if model == "Okumura":
            loss = self.okumura_model(freq, dist, h_t, h_r)
            equation_text = "Path Loss (dB) = 69.55 + 26.16 × log₁₀(distance) + 20 × log₁₀(frequency / 1e6)"
        elif model == ("Hata"):
            loss = self.hata_model(freq, dist, h_t, h_r, area)
            if area == "Urban":
                equation_text = "Path Loss (dB) = 69.55 + 26.16 * log10(Distance) - 13.82 * log10(Transmitter Height) - 4.78 * (log10(Frequency))^2 + (44.9 - 6.55 * log10(Transmitter Height)) * log10(Distance) + 18.33 * log10(Frequency) - 40.94"
            elif area == "Suburban":
                equation_text = "Path Loss (dB) = 69.55 + 26.16 * log10(Distance) + 13.82 * log10(Transmitter Height) - 4.78 * (log10(Frequency))^2 + (44.9 - 6.55 * log10(Transmitter Height)) * log10(Distance) + 18.33 * log10(Frequency) - 16.94"
            elif area == "Rural":
                equation_text = "Path Loss (dB) = 69.55 + 26.16 * log10(Distance) + 13.82 * log10(Transmitter Height) - 4.78 * (log10(Frequency))^2 + (44.9 - 6.55 * log10(Transmitter Height)) * log10(Distance) + 18.33 * log10(Frequency) - 4.78"
        elif model == "Free Space":
            loss = self.free_space_model(freq, dist)
            equation_text = "Path Loss (dB) = 20 × log₁₀(distance) + 20 × log₁₀(frequency) − 147.55"
        elif model == "CCIR":
            loss = self.ccir_model(freq, dist, h_t, h_r)
            equation_text = "Path Loss (dB) = 36.6 × log₁₀(distance) + 22.8 × log₁₀(frequency) + 27.2"
        
        self.plot_graph(dist, loss, model)

        self.equation_label.config(text=equation_text)

        self.power_loss_label.config(text="Power Loss of Receiver: " + str(loss[-1]) + " dB")

    def okumura_model(self, freq, dist, h_t, h_r):
        return 69.55 + 26.16 * np.log10(dist) - 13.82 * np.log10(h_t) - 4.78 * (np.log10(freq))**2  * np.log10(h_r)

    def hata_model(self, freq, dist, h_t, h_r, area):
        if area == "Urban":
            return 69.55 + 26.16 * np.log10(dist) + 13.82 * np.log10(h_t) - 4.78 * (np.log10(freq))**2 + (44.9 - 6.55 * np.log10(h_t)) * np.log10(dist) + 18.33 * np.log10(freq) - 40.94
        elif area == "Suburban":
            K = (1.1 * np.log10(freq) -0.7) * h_r - (1.56*np.log10(freq) - 0.8)
            return 69.55 + 26.16 * np.log10(dist) - 13.82 * np.log10(h_t) - 4.78 * (np.log10(freq))**2 + (44.9 - 6.55 * np.log10(h_t)) * np.log10(dist) + 18.33 * np.log10(freq) - K
        elif area == "Rural":
            return 69.55 + 26.16 * np.log10(dist) - 13.82 * np.log10(h_t) - 4.78 * (np.log10(freq))**2 + (44.9 - 6.55 * np.log10(h_t)) * np.log10(dist) + 18.33 * np.log10(freq) - 4.78

    def free_space_model(self, freq, dist):
        return 20 * np.log10(dist) + 20 * np.log10(freq) + 147.55

    def ccir_model(self, freq, dist, h_t, h_r):
        return 36.6 * np.log10(dist) + 22.8 * np.log10(freq) + 27.2

    def plot_graph(self, dist, loss, model):
        # Clear the previous plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Create a new plot
        fig, ax = plt.subplots()
        ax.plot(dist, loss)
        ax.set_title(f"{model} Propagation Loss")
        ax.set_xlabel("Distance (km)")
        ax.set_ylabel("Propagation Loss (dB)")
        ax.grid(True)

        # Convert the plot to a tkinter-compatible format
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand='True')
        #canvas.pack_propagate(False)

        toolbar = NavigationToolbar2Tk(canvas, self.plot_frame)
        toolbar.update()
        canvas.get_tk_widget().pack()
        
def main():
    root = tk.Tk()
    root.geometry('800x400')
    app = PropagationModelGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

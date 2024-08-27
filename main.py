import os
import tkinter
from tkinter import ttk
from functions import *

line = "\n"

root = tkinter.Tk()
root.title("Subnett Calculator")
root.geometry("900x600")  # Adjusted window size to prevent clipping

# Create a style
style = ttk.Style(root)

# Get the absolute path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
tcl_file_path = os.path.join(current_dir, "forest-dark.tcl")

# Import the tcl file using the absolute path
root.tk.call("source", tcl_file_path)

# Set the theme with the theme_use method
style.theme_use("forest-dark")

# Configure the grid to align widgets to the left
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)

# store address
address = tkinter.StringVar()
placeholder = "e.g., 192.168.1.1/24"
address.set(placeholder)

title = ttk.Label(root, text="Subnet Calculator", font=("Arial", 20))
title.grid(row=0, column=0, padx=10, pady=10, sticky='w')

# Create a frame to act as a clickable area around the entry box
clickable_frame = ttk.Frame(root)
clickable_frame.grid(row=1, column=0, padx=10, pady=(10, 5), sticky='w')  # Reduced bottom padding

# text in frame
enter_box = ttk.Frame(clickable_frame)
enter_box.grid(row=0, column=0, sticky='ew')

ip_entry = ttk.Entry(enter_box, textvariable=address, foreground='grey')
ip_entry.grid(row=0, column=0, padx=0, pady=0, sticky='w')
ip_entry.focus()


def on_focus_in(event):
    if address.get() == placeholder:
        ip_entry.delete(0, "end")
    ip_entry.config(foreground='white')


def on_focus_out(event):
    if not ip_entry.get():
        address.set(placeholder)
        ip_entry.config(foreground='grey')
    else:
        ip_entry.config(foreground='white')


ip_entry.bind("<FocusIn>", on_focus_in)
ip_entry.bind("<FocusOut>", on_focus_out)


def remove_focus(event):
    root.focus()


clickable_frame.bind("<Button-1>", remove_focus)

# Create a frame for the buttons
button_frame = ttk.Frame(root)
button_frame.grid(row=2, column=0, pady=(5, 10), sticky='w')  # Reduced top padding

# Create a button
button1 = ttk.Button(button_frame, text="Calculate")
button1.grid(row=0, column=0, padx=10, pady=2, sticky='w')


def reset_entry():
    address.set(placeholder)
    ip_entry.config(foreground='grey')
    output_label.config(text="")
    output_label_results.config(text="")
    output_label_binary.config(text="")


reset_button = ttk.Button(button_frame, text="Reset", command=reset_entry)
reset_button.grid(row=0, column=1, padx=5, pady=5, sticky='w')

# Create a frame for the output labels
output_frame = ttk.Frame(root)
output_frame.grid(row=1, column=1, rowspan=3, padx=10, pady=10, sticky='n')

# Create a label for output
output_label = ttk.Label(output_frame, text="", anchor='w', justify='left')
output_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
output_label.configure(foreground='#217346')

output_label_results = ttk.Label(output_frame, text="", anchor='w', justify='left')
output_label_results.grid(row=0, column=1, padx=10, pady=10, sticky='w')

output_label_binary = ttk.Label(output_frame, text="", anchor='w', justify='left')
output_label_binary.grid(row=0, column=2, padx=10, pady=10, sticky='w')


def print_ip_address(event=None):
    ip = ip_entry.get()
    if is_valid_ip(ip):
        # Split the IP address and the subnet mask
        ip_spl, mask_spl = ip.split("/", 1)
        # Convert the mask to decimal and binary
        decimal_mask, binary_mask = convert_mask(mask_spl)
        # Calculate the broadcast IP
        num_hosts = calculate_num_hosts(binary_mask)
        # Calculate the number of usable hosts
        num_usable_hosts = calculate_num_usable_hosts(num_hosts)

        # Convert the IP address to binary
        ip_binary = calculate_ip_binary(ip_spl)
        # Remove dots from the binary representations
        ip_binary_no_dots = ip_binary.replace('.', '')
        binary_mask_no_dots = binary_mask.replace('.', '')
        # Calculate the subnet ID
        subnet_id = calculate_subnet_id(ip_binary_no_dots, binary_mask_no_dots)
        # Convert the subnet ID to binary
        subnet_id_binary = calculate_ip_binary(subnet_id)

        # Calculate the wildcard mask
        wildcard_mask = calculate_wildcard_mask(decimal_mask)
        # Convert the wildcard mask to binary
        wildcard_mask_binary = calculate_ip_binary(wildcard_mask)

        # Calculate the broadcast IP
        broadcast_ip = calculate_broadcast_ip(ip_binary_no_dots, binary_mask_no_dots)
        # Calculate the first available IP
        # Convert the broadcast IP to binary
        broadcast_ip_binary = calculate_ip_binary(broadcast_ip)

        first_available_ip = calculate_first_available_ip(ip_binary_no_dots, binary_mask_no_dots)
        # Calculate the last available IP
        last_available_ip = calculate_last_available_ip(ip_binary_no_dots, binary_mask_no_dots)
        # Calculate the IP class
        ip_class = calculate_ip_class(ip_spl)
        # Calculate whether the IP is private or public
        ip_type = is_ip_private(ip_spl)
        # Calculate wildcard mask

        # Update the text of the label
        output_label.config(text=f"Address: {ip}\nNetmask: {decimal_mask}\nWildcard: {wildcard_mask}\n"
                                 f"Network: {subnet_id} ({ip_class})\nBroadcast: {broadcast_ip}\n"
                                 f"Hosts/Net: {num_usable_hosts}/{num_hosts}\nRange: {first_available_ip} - {last_available_ip}\n"
                                 f"Type: {ip_type}")

        # Update the text of the label
        output_label_results.config(text=f"{ip}\n{decimal_mask}\n{wildcard_mask}\n{subnet_id}\n{broadcast_ip}\n"
                                         f"{num_usable_hosts}/{num_hosts}\n{first_available_ip}")

        # Update the text of the label
        output_label_binary.config(text=f"{calculate_ip_binary(ip_spl)}\n{binary_mask}\n{wildcard_mask_binary}\n"
                                        f"{subnet_id_binary}\n{broadcast_ip_binary}\n{ip_type}\n{last_available_ip}")

        print(f"\nIp: {ip}\n"
              f"Ip Binary: {calculate_ip_binary(ip_spl)}\n"
              f"Mask: {decimal_mask}\n"
              f"Mask Binary: {binary_mask}"
              f"\nSubnet ID: {subnet_id}"
              f"\nBroadcast: {broadcast_ip}"
              f"\nHosts: {num_hosts}"
              f"\nUsable Hosts: {num_usable_hosts}"
              f"\nRange: {first_available_ip} - {last_available_ip}"
              f"\nClass: {ip_class}"
              f"\nIP Type: {ip_type}")
    else:
        # Reset other output labels
        output_label_results.config(text="")
        output_label_binary.config(text="")
        # Set the error message
        output_label.config(text="Invalid IP address. Please try again. \nUse the format: 192.168.2.1/24")


# Assign the command to the button
button1.config(command=print_ip_address)
root.bind('<Return>', print_ip_address)
root.mainloop()

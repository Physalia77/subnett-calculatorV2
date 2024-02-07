import tkinter
from tkinter import ttk
import sv_ttk

from functions import *

line = "\n"

root = tkinter.Tk()
root.title("Subnett Calculator")
root.geometry("600x400")
sv_ttk.set_theme("dark")
ttk.Label(root, text="Welcome to my Subnet Calculator!").grid(row=0, column=0, columnspan=2)

button = ttk.Button(root, text="Toggle theme", command=sv_ttk.toggle_theme)
button.grid(row=0, column=4)

# store address
address = tkinter.StringVar()

# text in frame
enter_box = ttk.Frame(root)
enter_box.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='ew')

# address
ip_label = ttk.Label(enter_box, text="Input your IP and subnet mask:")
ip_label.grid(row=0, column=0, sticky='ew')

ip_entry = ttk.Entry(enter_box, textvariable=address)
ip_entry.grid(row=1, column=0, sticky='ew')
ip_entry.focus()

# Create a button
button1 = ttk.Button(root, text="Calculate")
button1.grid(row=2, column=0, columnspan=3)

# Create a label for output
output_label = ttk.Label(enter_box, text="", anchor='w', justify='left', font=('defualt', 10))
output_label.grid(row=4, column=0, columnspan=3, sticky='ew')

output_label_results = ttk.Label(enter_box, text="", anchor='w', justify='left', font=('defualt', 10))
output_label_results.grid(row=4, column=1, columnspan=3, sticky='ew')


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

        # Calculate the broadcast IP
        broadcast_ip = calculate_broadcast_ip(ip_binary_no_dots, binary_mask_no_dots)
        # Calculate the first available IP
        first_available_ip = calculate_first_available_ip(ip_binary_no_dots, binary_mask_no_dots)
        # Calculate the last available IP
        last_available_ip = calculate_last_available_ip(ip_binary_no_dots, binary_mask_no_dots)
        # Calculate the IP class
        ip_class = calculate_ip_class(ip_spl)
        # Calculate whether the IP is private or public
        ip_type = is_ip_private(ip_spl)
        # Calculate wildcard mask
        wildcard_mask = calculate_wildcard_mask(binary_mask_no_dots)

        # Update the text of the label
        output_label.config(text=f"\nAddress:\n"
                                 f"IP Binary\n"
                                 f"Mask\n"
                                 f"Mask Binary"
                                 f"\nSubnet ID"
                                 f"\nBroadcast"
                                 f"\nHosts"
                                 f"\nUsable Hosts"
                                 f"\nRange"
                                 f"\nClass"
                                 f"\nIP Type")

        # Update the text of the label
        output_label_results.config(text=f"\n{ip}\n"
                                         f"{calculate_ip_binary(ip_spl)}\n"
                                         f"{decimal_mask}\n"
                                         f"{binary_mask}"
                                         f"\n{subnet_id}"
                                         f"\n{broadcast_ip}"
                                         f"\n{num_hosts}"
                                         f"\n{num_usable_hosts}"
                                         f"\n{first_available_ip} - {last_available_ip}"
                                         f"\n{ip_class}"
                                         f"\n{ip_type}")

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
        output_label.config(text="Invalid IP address. Please try again. \nUse the format: 192.168.2.1/24")


# Assign the command to the button
button1.config(command=print_ip_address)
root.bind('<Return>', print_ip_address)
root.mainloop()

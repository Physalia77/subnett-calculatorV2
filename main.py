import tkinter
from tkinter import ttk
import sv_ttk


from functions import *

line = "\n"

root = tkinter.Tk()
root.title("Subnett Calculator")
root.geometry("660x440")
# Create a style
style = ttk.Style(root)

# Import the tcl file
root.tk.call("source", "forest-dark.tcl")

# Set the theme with the theme_use method
style.theme_use("forest-dark")

# store address
address = tkinter.StringVar()

# text in frame
enter_box = ttk.Frame(root)
enter_box.grid(row=1, column=0, columnspan=5, padx=10, pady=40, sticky='ew')

ip_entry = ttk.Entry(enter_box, textvariable=address)
ip_entry.grid(row=1, column=0, sticky='ew')
ip_entry.focus()

# Create a button
button1 = ttk.Button(root, text="Calculate")
button1.grid(row=2, column=0, columnspan=3)

# Create a label for output
output_label = ttk.Label(enter_box, text="", anchor='w', justify='left')
output_label.grid(row=4, column=0, sticky='n')
output_label.configure(foreground='#217346')

output_label_results = ttk.Label(enter_box, text="", anchor='w', justify='left')
output_label_results.grid(row=4, column=1, sticky='n')

output_label_binary = ttk.Label(enter_box, text="", anchor='w', justify='left')
output_label_binary.grid(row=4, column=4, sticky='n')


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
        output_label.config(text=f"\nAddress:\n"  # IP + binary
                                 f"Netmask\n"  # Mask + binary
                                 f"Wildcard\n"  # Wildcard mask + binary
                                 f"\nNetwork"  # Subnet ID + Class
                                 f"\nBroadcast"  # Broadcast IP + Broadcast binary
                                 f"\nHosts/Net"  # Hosts and usable hosts + Private or Public
                                 f"\nRange")  # First and last available IP

        # Update the text of the label
        output_label_results.config(text=f"\n{ip}       \n"
                                         f"{decimal_mask}       \n"
                                         f"{wildcard_mask}      \n"
                                         f"\n{subnet_id}        "
                                         f"\n{broadcast_ip}         "
                                         f"\n{num_usable_hosts}/{num_hosts}         "
                                         f"\n{first_available_ip}       ")

        # Update the text of the label
        output_label_binary.config(text=f"\n{calculate_ip_binary(ip_spl)}\n"
                                        f"{binary_mask}\n"
                                        f"{wildcard_mask_binary}\n"
                                        f"\n{subnet_id_binary}      {ip_class}"
                                        f"\n{broadcast_ip_binary}"
                                        f"\n{ip_type}"
                                        f"\n{last_available_ip}")

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

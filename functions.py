# Description: This file contains the functions used to calculate the IP address details.
def calculate_ip_binary(ip_parts):
    return '.'.join([bin(int(x) + 256)[3:] for x in ip_parts.split('.')])


# Check if the IP address is valid
def is_valid_ip(ip):
    if '/' not in ip:
        return False
    try:
        ip, mask = ip.split('/')
        octets = ip.split('.')
        if len(octets) != 4:
            return False
        for octet in octets:
            if not (0 <= int(octet) <= 255):
                return False
        if not (1 <= int(mask) <= 32):
            return False
        return True
    except ValueError:
        return False


# Convert the subnet mask to decimal and binary
def convert_mask(mask):
    # Calculate the number of '1' bits in the subnet mask
    ones = int(mask)
    # Create a binary string with the number of '1' bits followed by '0' bits
    binary_mask = '1' * ones + '0' * (32 - ones)
    # Split the binary string into octets
    binary_octets = [binary_mask[i:i + 8] for i in range(0, 32, 8)]
    # Convert each octet to decimal and join them with '.'
    decimal_mask = '.'.join([str(int(octet, 2)) for octet in binary_octets])
    # Convert each decimal octet to binary and join them with '.'
    binary_mask = '.'.join([bin(int(octet, 2))[2:].zfill(8) for octet in binary_octets])
    return decimal_mask, binary_mask


# Calculate the number of hosts
def calculate_num_hosts(mask_binary):
    # Count the number of zeros in the mask
    num_zeros = mask_binary.count('0')
    # Calculate the number of hosts
    num_hosts = int(2 ** int(num_zeros))
    return num_hosts


# Calculate the number of usable hosts
def calculate_num_usable_hosts(num_hosts):
    # Calculate the number of usable hosts
    num_usable_hosts = num_hosts - 2
    return num_usable_hosts


# Calculate the subnet mask
def calculate_subnet_mask(sm):
    return ".".join(sm[i:i + 8] for i in range(0, len(sm), 8))

# Calculate the wildcard mask
def calculate_wildcard_mask(subnet_mask):
    # Split the subnet mask into octets
    octets = subnet_mask.split('.')
    # Subtract each octet from 255 to get the wildcard mask
    wildcard_octets = [str(255 - int(octet)) for octet in octets]
    # Join the resulting octets with a dot
    wildcard_mask = '.'.join(wildcard_octets)
    return wildcard_mask


# Calculate the subnet ID
def calculate_subnet_id(ip_binary, mask_binary):
    # Perform a bitwise AND operation on IP and mask to get the Subnet ID
    subnet_id_binary = ''.join(str(int(ip_bit) & int(mask_bit)) for ip_bit, mask_bit in zip(ip_binary, mask_binary))
    # Convert the binary subnet ID back to dotted-decimal format
    subnet_id = '.'.join([str(int(subnet_id_binary[i:i + 8], 2)) for i in range(0, len(subnet_id_binary), 8)])
    return subnet_id


# Calculate the broadcast IP
def calculate_broadcast_ip(ip_binary, mask_binary):
    # Convert IP and mask binary strings to lists for easy manipulation
    ip_list = list(ip_binary)
    mask_list = list(mask_binary)

    # Count the number of zeros in the mask
    num_zeros = mask_binary.count('0')

    # Replace rightmost zeros in IP with ones from the mask
    for i in range(-1, -(num_zeros + 1), -1):
        if mask_list[i] == '0':
            ip_list[i] = '1'

    # Convert the list back to a string
    broadcast_binary = ''.join(ip_list)

    # Output the binary broadcast IP address
    broadcast = '.'.join([str(int(broadcast_binary[i:i + 8], 2)) for i in range(0, len(broadcast_binary), 8)])

    return broadcast


# Calculate the first available IP address
def calculate_first_available_ip(ip_binary, mask_binary):
    # Convert IP and mask binary strings to lists for easy manipulation
    ip_list = list(ip_binary)
    mask_list = list(mask_binary)

    # Count the number of zeros in the mask
    num_zeros = mask_binary.count('0')

    # Replace rightmost zeros in IP with zeros from the mask
    for i in range(-1, -(num_zeros + 1), -1):
        if mask_list[i] == '0':
            ip_list[i] = '0'

    # Convert the list back to a string
    network_binary = ''.join(ip_list)

    # Calculate the first available IP address by incrementing the network address by 1
    first_available_binary = bin(int(network_binary, 2) + 1)[2:].zfill(32)

    # Output the binary representation of the first available IP address
    first_available_ip = '.'.join(
        [str(int(first_available_binary[i:i + 8], 2)) for i in range(0, len(first_available_binary), 8)])
    return first_available_ip


# Calculate the last available IP address
def calculate_last_available_ip(ip_binary, mask_binary):
    # Convert IP and mask binary strings to lists for easy manipulation
    ip_list = list(ip_binary)
    mask_list = list(mask_binary)

    # Count the number of zeros in the mask
    num_zeros = mask_binary.count('0')

    # Replace rightmost zeros in IP with ones from the mask
    for i in range(-1, -(num_zeros + 1), -1):
        if mask_list[i] == '0':
            ip_list[i] = '1'

    # Convert the list back to a string
    broadcast_binary = ''.join(ip_list)

    # Calculate the last available IP address by decrementing the broadcast address by 1
    last_available_binary = bin(int(broadcast_binary, 2) - 1)[2:].zfill(32)

    # Output the binary representation of the last available IP address
    last_available_ip = '.'.join(
        [str(int(last_available_binary[i:i + 8], 2)) for i in range(0, len(last_available_binary), 8)])
    return last_available_ip


# check if ip is private or public, by checking if the ip falls anywhere in the private ip range below.
# Class A Private IP Range: 10.0.0.0 – 10.255.255.255
#
# Class B Private IP Range: 172.16.0.0 – 172.31.255.255
#
# Class C Private IP Range: 192.168.0.0 – 192.168.255.25
# Constants for IP ranges
CLASS_A_PRIVATE_IP_RANGE = (10, 10, 255, 255)
CLASS_B_PRIVATE_IP_RANGE = (172, 16, 172, 31)
CLASS_C_PRIVATE_IP_RANGE = (192, 168, 192, 168)


# Check if the IP is private or public
def is_ip_private(ip_spl):
    ip_spl = ip_spl.split(".")
    ip_spl = list(map(int, ip_spl))
    if ip_spl[0] == CLASS_A_PRIVATE_IP_RANGE[0]:
        return "Private"
    elif ip_spl[0] == CLASS_B_PRIVATE_IP_RANGE[0] and CLASS_B_PRIVATE_IP_RANGE[1] <= ip_spl[1] <= \
            CLASS_B_PRIVATE_IP_RANGE[2]:
        return "Private"
    elif ip_spl[0] == CLASS_C_PRIVATE_IP_RANGE[0] and ip_spl[1] == CLASS_C_PRIVATE_IP_RANGE[1]:
        return "Private"
    else:
        return "Public"


# Calculate the IP class
def calculate_ip_class(ip_spl):
    ip_binary = calculate_ip_binary(ip_spl)

    if ip_binary[:1] == "0":
        return "Class A"
    if ip_binary[:2] == "10":
        return "Class B"
    if ip_binary[:3] == "110":
        return "Class C"
    if ip_binary[:4] == "1110":
        return "Class D"
    if ip_binary[:4] == "1111":
        return "Class E"

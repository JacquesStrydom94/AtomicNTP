import customtkinter as tk
import socket
import struct
import time

def create_ntp_packet():
    ntp_packet = bytearray(48)
    ntp_packet[0] = 0x1B  # Leap Indicator: 0 (no warning), Version Number: 4 (NTPv4), Mode: 3 (Client)
    return ntp_packet

def get_ntp_time(server_ip):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
            client_socket.settimeout(10)
            client_socket.connect((server_ip, 123))
            ntp_packet = create_ntp_packet()
            client_socket.send(ntp_packet)
            response = client_socket.recv(48)
            ntp_time = struct.unpack("!12I", response)[10]
            unix_time = ntp_time - 2208988800
            return unix_time
    except Exception as e:
        print(f"Error fetching NTP time: {e}")
        return None

def update_time_label():
    unix_time = get_ntp_time("129.6.15.28")
    if unix_time:
        gmt_plus_2_time = time.gmtime(unix_time + 2 * 3600)
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', gmt_plus_2_time)
        time_label.configure(text=f"GMT+2 Time: {formatted_time}")
    else:
        time_label.configure(text="Error fetching NTP time")
    root.after(1, update_time_label)  # Update every 1 millisecond

root = tk.CTk()
root.title("Atomic Clock Time (GMT+2)")

# Set the appearance mode to follow the system theme
tk.set_appearance_mode("system")

time_label = tk.CTkLabel(root, font=("Helvetica", 16))
time_label.pack(pady=20)

update_time_label()  # Start updating the time label

root.mainloop()

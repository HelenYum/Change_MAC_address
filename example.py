import string
import random
import subprocess
import re
import argparse
# uppercased_hexdigits = ''.join(set(string.hexdigits.upper()))  # получаем mac и переводим буквы в верхний регистр
# mac = ""
# for i in range(6):
#     for j in range(2):
#         if i == 0:
#             mac += random.choice("012345678ACDEF")
#         else:
#             mac += random.choice(uppercased_hexdigits)
#     mac += ":"
#
# # print(mac.strip(":"))


# iface="vmenet2"
#
# output = subprocess.check_output(f"ifconfig {iface}", shell=True).decode()
# a = re.search(r'ether \w\w:\w\w:\w\w:\w\w:\w\w:\w\w', output).group().split()[1] #.strip()
# print(a)
def get_random_mac_address():
    print("get_random_mac_address()")

def get_current_mac_address():
    print("get_current_mac_address")

parser = argparse.ArgumentParser(description="Mac Changer on Linux")
parser.add_argument("-i", "--interface", help="The network interface name")
parser.add_argument("-r", "--random", action="store_true", help="Whether to generate a random MAC address")
parser.add_argument("-m", "--mac", help="The new MAC you want to change to")
args = parser.parse_args()
iface = args.interface
# print(args.mac)

if args.random:
    # генерируем случайный mac (вызываем функцию get_random_mac_address())
    get_random_mac_address()
elif args.mac:
    # устанавливаем пользовательский MAC
    new_mac_address = args.mac
    print(new_mac_address)

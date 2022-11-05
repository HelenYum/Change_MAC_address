#!/usr/bin/env python
import string
import subprocess
import re
import random
import argparse

# return mac address
def get_random_mac_address():
    """Генерируем и возвращаем mac адрес (Linux)"""
    uppercased_hexdigits = ''.join(set(string.hexdigits.upper()))  # получаем mac и переводим буквы в верхний регистр
    mac = ""
    for i in range(6):
        for j in range(2):
            if i == 0:
                mac += random.choice("012345678ACDEF")
            else:
                mac += random.choice(uppercased_hexdigits)
        mac += ":"
    return mac.strip(":")  # strip(":") удаляет начальные и конечные переданные значения

# return object class Argparse (interface, random, mac)
def get_arguments():  # получаем переменные от пользователя
    """
    The function receives mac address and interface from users
    :param parser: it's an instance of class OptionParser.
    We add this class in order to check the inout user's data for correctness.
    :param if elif: if the user enters an incorrect interface or MAC address, an error message is displayed on the screen
    :return options: the function returns the received variables
    """
    parser = argparse.ArgumentParser(
        description="Mac Changer on Linux")  # Парсит все что вводит пользователь, для предотвращения ошибок
    parser.add_argument("-i", "--interface", help="The network interface name")
    parser.add_argument("-r", "--random", action="store_true", help="Whether to generate a random MAC address")
    parser.add_argument("-m", "--mac", help="The new MAC you want to change to")
    args = parser.parse_args()
    if not args.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    # elif not args.mac or args.random:
    #     parser.error("[-] Please specify an MAC address, use --help for more info.")
    return args

# change mac address
def change_mac(interface, new_mac):
    """
    The function performs the change of the mac address
    :param interface: variable received from the user
    :param new_mac: variable received from the user
    :return: the function doesn't return anything, it only executes.
    """
    print("[+] Change MAC address for " + interface + " to " + new_mac)
    # отключаем интерфейс
    subprocess.check_output(f"ifconfig {interface} down", shell=True)
    # меняем MAC
    subprocess.check_output(f"ifconfig {interface} hw ether {new_mac}")
    # снова включаем сетевой интерфейс
    subprocess.check_output(f"ifconfig {interface} up", shell=True)

#return mac address on this laptop
def get_current_mac(interface):
    "используем команду ifconfig для получения инфы об интерфейсе и MAC адресе"
    output = subprocess.check_output(f"ifconfig {interface}",
                                     shell=True).decode()  # получаем данные по конкретному интерфейсу
    mac_address_search_result = re.search(r'ether \w\w:\w\w:\w\w:\w\w:\w\w:\w\w', output)
    if mac_address_search_result:
        return mac_address_search_result.group().split()[1].strip()  # возвращаем очищенный MAC
    else:
        print("[-] Could not read MAC address.")


options = get_arguments()  # take users arguments
iface = options.interface
if options.random:
    # генерируем случайный mac (вызываем функцию get_random_mac_address())
    new_mac = get_random_mac_address()

elif options.mac:
    # устанавливаем пользовательский MAC
    new_mac = options.mac


old_mac_address = get_current_mac(iface)
print("[*] Old MAC address:", old_mac_address)

change_mac(iface, new_mac)

# проверяем реально ли поменялся MAC
new_mac_address_1 = get_current_mac(options.interface)
print("[+] New MAC address:", new_mac_address_1)

# options = get_arguments()  # take users arguments
# current_mac = get_current_mac(options.interface)
# print("Current MAC = " + str(current_mac))
#
# change_mac(options.interface, options.new_mac)
# current_mac = get_current_mac(options.interface)
#
# if current_mac == options.new_mac:
#     print("[+] MAC address was successfully changed to " + current_mac)
# else:
#     print("[-] MAC address didn't get changed.")

# print(get_arguments().__doc__)
# print(change_mac().__doc__)

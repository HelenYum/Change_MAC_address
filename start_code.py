import subprocess
import string
import random
import re
import argparse


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
    return mac.strip(":")   #strip(":") удаляет начальные и конечные переданные значения


def get_current_mac_address(interface):
    "используем команду ifconfig для получения инфы об интерфейсе и MAC адресе"
    output = subprocess.check_output(f"ifconfig {interface}", shell=True).decode()  #получаем данные по конкретному интерфейсу
    # check_output запускает команду, которую мы передаем, и возвращает вывод
    return re.search(r'ether \w\w:\w\w:\w\w:\w\w:\w\w:\w\w', output).group().split()[1].strip() #возвращаем очищенный MAC


def change_mac_address(iface, new_mac_address):
    # отключаем интерфейс
    subprocess.check_output(f"ifconfig {iface} down", shell=True)
    # меняем MAC
    subprocess.check_output(f"ifconfig {iface} hw ether {new_mac_address}")
    # снова включаем сетевой интерфейс
    subprocess.check_output(f"ifconfig {iface} up", shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mac Changer on Linux")
    parser.add_argument("-i", "--interface", help="The network interface name")
    parser.add_argument("-r", "--random", action="store_true", help="Whether to generate a random MAC address")
    parser.add_argument("-m", "--mac", help="The new MAC you want to change to")
    args = parser.parse_args()
    iface = args.interface

    if args.random:
        # генерируем случайный mac (вызываем функцию get_random_mac_address())
        new_mac_address = get_random_mac_address()
    elif args.mac:
        # устанавливаем пользовательский MAC
        new_mac_address = args.mac

    old_mac_address = get_current_mac_address(iface)
    print("[*] Old MAC address:", old_mac_address)

    change_mac_address(iface, new_mac_address)
    # проверяем реально ли поменялся MAC
    new_mac_address = get_current_mac_address(iface)
    print("[+] New MAC address:", new_mac_address)

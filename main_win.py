"""
In this program we use 3 windows commands:
getmac -> возвращает список сетевых интерфейсов
reg -> взаимодействие с реестром
wmic -> вкл/откл сетевого адаптера
"""
import subprocess
import regex as re
import string
import random
import argparse

# пут в реестре, где находятся сведения о сетевом интерфейсе
network_interface_reg_path = r"HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}"
transport_name_regex = re.compile("{.+}")
# Регулярное выражение MAC address
mac_address_regex = re.compile(r"([A-Z0-9]{2}[:-]){5}([A-Z0-9]{2})")


def get_random_mac_address():
    uppercased_hexdigits = "".join(set(string.hexdigits.upper()))
    return random.choice(uppercased_hexdigits) + random.choice("24AE") + "".join(
        random.sample(uppercased_hexdigits, k=10))


def clean_mac(mac):
    return "".join(c for c in mac if c in string.hexdigits).upper()


def get_connected_adapters_mac_address():
    connected_adapters_mac = []
    for potential_mac in subprocess.check_output("getmac").decode().splitlines():
        mac_address = mac_address_regex.search(potential_mac)
        transport_name = transport_name_regex.search(potential_mac)
        if mac_address and transport_name:
            connected_adapters_mac.append((mac_address.group(), transport_name.group()))
    return connected_adapters_mac


def get_user_adapter_choice(connected_adapters_mac):
    # вывод доступных адаптеров
    for i, option in enumerate(connected_adapters_mac):
        print(f"#{i}: {option[0]}, {option[1]}")
    if len(connected_adapters_mac) <= 1:
        return connected_adapters_mac[0]

    # выбор пользователем сетевого адаптера
    try:
        choice = int(input("Pleae choose the interface you want to change the MAC address:"))
        return connected_adapters_mac[choice]
    except:
        print("Not a valid choice, guitting....")
        exit()


def change_mac_address(adapter_transport_name, new_mac_address):
    # используем команду reg QUERY, для получения поступных адаптеров из реестра
    output = subprocess.check_output(f"reg QUERY " + network_interface_reg_path.replace("\\\\", "\\")).decode()
    for interface in re.findall(rf"{network_interface_reg_path}\\\d+", output):
        adapter_index = int(interface.split("\\")[-1])
        interface_content = subprocess.check_output(f"reg QUERY {interface.strip()}").decode()
        # если имя адапрера найдено в выходн. данных reg QUERY,
        # то это тот адаптер который мы ищем
        # меняем MAC с помощью команды reg ADD
        if adapter_transport_name in interface_content:
            changing_mac_output = subprocess.check_output(
                f"reg add {interface} /v NetworkAddress /d {new_mac_address} /f").decode()
            print(changing_mac_output)
            # выходим из цикла
            break
    return adapter_index  # возвращаем индекс адаптера в котором изменили MAC

# отключаем и включаем адаптер
def disable_adapter(adapter_index):
    # используем комманду wmic для отключения адаптера
    disable_output = subprocess.check_output(f"wmic path win32_networkadapter where index={adapter_index} call disable").decode()
    return disable_output

def enable_adapter(adapter_index):
    enable_output = subprocess.check_output(f"wmic path win32_networkadapter where index={adapter_index} call enable").decode()
    return enable_output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python Windows MAC change")
    parser.add_argument("-r", "--random", action="store_true", help="Whether a generate a random MAC address")
    parser.add_argument("-m", "--mac", help="The new MAC you want to change to")
    args = parser.parse_args()
    if args.random:
        new_mac_address = get_random_mac_address()
    elif args.mac:
        new_mac_address = clean_mac(args.mac)

    connected_adapters_mac = get_connected_adapters_mac_address()
    old_mac_address, target_transport_name = get_user_adapter_choice(connected_adapters_mac)
    print("[*] Old MAC address: ", old_mac_address)
    adapter_index = change_mac_address(target_transport_name, new_mac_address)
    print("[+] Changed to: ", new_mac_address)
    disable_adapter(adapter_index)
    print("[+] Adapter is disabled")
    enable_adapter(adapter_index)
    print("[+] Adapter is enabled again")
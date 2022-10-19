import keyboard

def main():

    while True:
        event = keyboard.read_event()
        print("Key Name: ")
        print(event.name)
        print("Scan code: ")
        print(keyboard.key_to_scan_codes(event.name))
        print()
        print()

main()
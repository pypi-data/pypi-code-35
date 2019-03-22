import sys
import time
import math
import psutil


class bcolors:
    PINK = "\033[95m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


network_interface = "en0"

counters = psutil.net_io_counters(pernic=True)
bytes_received_for_counters = [(c, counters[c][1]) for c in counters.keys()]
network_interface = list(counters.keys())[0]
max = 0
for nib in bytes_received_for_counters:
    if nib[0] == 'lo':
        continue
    if nib[1] > max:
        max = nib[1]
        network_interface = nib[0]


def get_current_bytes():
    data = psutil.net_io_counters(pernic=True)[network_interface]
    down_bytes = data.bytes_recv
    up_bytes = data.bytes_sent
    return down_bytes, up_bytes


def format_speed(speed, ps):
    if speed == 0:  # log(0) will error out
        return "0 B" + ("/s" if ps else "")
    factor = int(math.floor(math.log(speed) / math.log(1024)))
    return (
        str(int(speed / 1024 ** factor))
        + " "
        + ["B", "KB", "MB", "GB", "TB", "PB"][factor]
        + ("/s" if ps else "")
    )


def print_speed(down_speed, up_speed, final=False, ps=True):
    CURSOR_UP_ONE = "\x1b[1A"
    ERASE_LINE = "\x1b[2K"
    sys.stdout.write(
        "\rDown: %s%s%s\n\r  Up: %s%s%s\n"
        % (
            bcolors.GREEN,
            format_speed(down_speed, ps),
            bcolors.ENDC,
            bcolors.BLUE,
            format_speed(up_speed, ps),
            bcolors.ENDC,
        )
    )
    if not final:
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)


def main():
    global network_interface
    if len(sys.argv) > 1:
        network_interface = sys.argv[1]
    print("Interface:", network_interface)
    start_time = time.time()
    start_down_bytes, start_up_bytes = get_current_bytes()
    last_down_bytes, last_up_bytes = start_down_bytes, start_up_bytes
    last_time = start_time

    down_speed = 0
    up_speed = 0

    try:
        while True:
            print_speed(down_speed, up_speed)
            time.sleep(1)

            down_bytes, up_bytes = get_current_bytes()
            now = time.time()

            down_speed = (last_down_bytes - down_bytes) / (last_time - now)
            up_speed = (last_up_bytes - up_bytes) / (last_time - now)

            last_down_bytes, last_up_bytes = down_bytes, up_bytes
            last_time = now
    except KeyboardInterrupt:
        print("\rAverage speed")
        down_bytes, up_bytes = get_current_bytes()
        now = time.time()
        down_speed = (down_bytes - start_down_bytes) / (now - start_time)
        up_speed = (up_bytes - start_up_bytes) / (now - start_time)
        print_speed(down_speed, up_speed, True)

        print("\nTotal data")
        down_bytes, up_bytes = get_current_bytes()
        down_speed = down_bytes - start_down_bytes
        up_speed = up_bytes - start_up_bytes
        print_speed(down_speed, up_speed, True, False)


if __name__ == "__main__":
    main()

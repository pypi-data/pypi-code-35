#!/usr/bin/python3

"""
KatFetch
Minimal and customizable information tool
By Kat Hamer
"""

import os              # Get environment variables
import platform        # Get platform information
import cpuinfo         # Get CPU info
import click           # Handle command line arguments
import distro          # Get Linux distribution
import get_shell       # Get shell version
import memory          # Get memory info
import get_wm          # Get window manager

def color_entry(title, value, accent):
    """Format an entry with a coloured accent"""
    title = click.style(title, fg=accent)
    return f"{title} {value}"


def display_bar(length, showbg, block_char, bar_height, fg):
    """Output a bar of coloured blocks"""
    for _ in range(bar_height):
        for color in list(click.termui._ansi_colors.keys())[showbg:length]:
            if fg:
                click.secho(block_char, fg=color, nl=False)
            else:
                  click.secho(block_char, bg=color, nl=False)
        print()  # Print a newline


def get_info():
    """Get info to display"""
    return {"os": f"{platform.system()} {platform.release()}",
            "hostname": platform.node(),
            "user": os.getenv("USER"),
            "term": os.getenv("TERM"),
            "shell": get_shell.version(),
            "distro": distro.name(),
            "mem_used": memory.used(),
            "mem_total": memory.total(),
            "mem_usage": f"{memory.used()}/{memory.total()}",
            "processor": cpuinfo.get_cpu_info()["brand"],
            "wm": get_wm.wm()
            }


@click.command()
@click.option("--color", default="blue", help="Accent color.")
@click.option("--nobar", is_flag=True, default=False, help="Don't show bar.")
@click.option("--barlen", default=8, help="Number of colour blocks to display.")
@click.option("--showbg", is_flag=True, default=True, help="Show background colour block in colour bar.")
@click.option("--block", default=" "*5, help="Block character to use in bar.")
@click.option("--height", default=2, help="Height of bar.")
@click.option("--fg", is_flag=True, default=False, help="Colour the foreground of the block character.")
def main(color, nobar, barlen, showbg, block, height, fg):
    """Main function"""
    if color not in click.termui._ansi_colors.keys():
        print(f"Error: {color} is not a valid colour.\nPlease specify one of:")
        print("\n".join(click.termui._ansi_colors.keys()))
        exit(1)

    info = get_info()

    entries = [color_entry("User", info["user"], color),
               color_entry("OS", info["os"], color),
               color_entry("Distro", info["distro"], color),
               color_entry("Hostname", info["hostname"], color),
               color_entry("Terminal", info["term"], color),
               color_entry("Shell", info["shell"], color),
               color_entry("Memory", info["mem_usage"], color),
               color_entry("CPU", info["processor"], color),
               color_entry("WM", info["wm"], color),
               ""]

    for entry in entries:
        print(entry)

    if not nobar:
        display_bar(barlen, showbg, block, height, fg)

if __name__ == "__main__":
    main()

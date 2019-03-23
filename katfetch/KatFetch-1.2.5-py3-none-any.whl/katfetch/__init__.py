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

def display_entry(title, value, accent):
    """Format and display an entry"""
    if accent:
        title = click.style(title, fg=accent)
    print(f"{title} {value}")


def display_bar(length, showbg, block_char, bar_height, fg):
    print()  # Print a newline
    """Output a bar of coloured blocks"""
    for _ in range(bar_height):
        for color in list(click.termui._ansi_colors.keys())[showbg:length]:
            if fg:
                click.secho(block_char, fg=color, nl=False)
            else:
                  click.secho(block_char, bg=color, nl=False)
        print()  # Print a newline

display_entry

def display_entries(color):
    """Display each entry as soon as the required information is available"""
    display_entry("OS", f"{platform.system()} {platform.release()}", color)
    display_entry("Hostname", platform.node(), color)
    display_entry("User", os.getenv("USER"), color)
    display_entry("Terminal", os.getenv("TERM"), color)
    display_entry("Shell", get_shell.version(), color)
    display_entry("Distro", distro.name(), color)
    display_entry("RAM", f"{memory.used()}/{memory.total()}", color)
    display_entry("CPU", cpuinfo.get_cpu_info()["brand"], color)
    display_entry("WM", get_wm.wm(), color)

@click.command()
@click.option("--color", default="blue", help="Accent color.")
@click.option("--nobar", is_flag=True, default=False, help="Don't show bar.")
@click.option("--barlen", default=8, help="Number of colour blocks to display.")
@click.option("--showbg", is_flag=True, default=True, help="Show background colour block in colour bar.")
@click.option("--block", default=" "*5, help="Block character to use in bar.")
@click.option("--height", default=2, help="Height of bar.")
@click.option("--fg", is_flag=True, default=False, help="Colour the foreground of the block character.")
@click.option("--nocol", is_flag=True, default=False, help="Disable accent colours.")
@click.option("--stdout", is_flag=True, default=False, help="Combine --nobar and --nocol to output text with no fancy formatting.")
def main(color, nobar, barlen, showbg, block, height, fg, nocol, stdout):
    """Main function"""
    if os.name == "nt":
        print("Error: KatFetch does not work on Windows. KatFetch is made for Unix like operating systems and works best on Linux. If you'd like help installing Linux, you can take a look at https://reddit.com/r/linux4noobs")
        exit(1)
    
    """Initialise colours"""
    if nocol or stdout:
        color = None
    elif color not in click.termui._ansi_colors.keys():
        print(f"Error: {color} is not a valid colour.\nPlease specify one of:")
        print("\n".join(click.termui._ansi_colors.keys()))
        exit(1)

    """Display entries"""
    display_entries(color)

    """Display the bar if it is enabled"""
    if not nobar and not stdout:
        display_bar(barlen, showbg, block, height, fg)

if __name__ == "__main__":
    main()

"""
Memory
Wrapper around psutil to get human readable memory stats
By Kat Hamer
"""

import psutil          # Get memory statistics
import hurry.filesize  # Convert to human readable format


def used():
    """Get used memory"""
    memory_object = psutil.virtual_memory()
    used_memory = memory_object.used
    human_readable = hurry.filesize.size(used_memory, system=hurry.filesize.si)
    return human_readable


def total():
    """Get total memory"""
    memory_object = psutil.virtual_memory()
    total_memory = memory_object.total
    human_readable = hurry.filesize.size(total_memory, system=hurry.filesize.si)
    return human_readable

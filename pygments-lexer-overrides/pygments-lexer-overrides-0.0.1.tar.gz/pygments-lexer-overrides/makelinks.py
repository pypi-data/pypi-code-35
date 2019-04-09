import os
import sys

# Retrieve an array of package paths.
paths = sys.path
found_pygments = False

# Examine each path for the existence of the package "pygments"
for package_path in paths:
    candidate = package_path + "/pygments/lexers"
    if (os.path.isdir(candidate)):
        print("Found pygments/lexers/ in path directory " + package_path)
        found_pygments = True
        break

# If we found pygments in the path, continue; otherwise, bail.    
if not found_pygments:
    print ("Could not find Pygments. Is it installed on this machine or virtual environment?")
    sys.exit(-1)

# Rename the existing pygments lexers.
try:
    os.rename(candidate + "/templates.py",candidate + "/templates.py.old")
    os.rename(candidate + "/css.py",candidate + "/css.py.old")
except OSError as e:
    print ("Could not rename " + e.filename + ". " + e.strerror)
    sys.exit(-2)

# Provide symbolic link from original pygments lexers to the custom ones inside this package.
try: 
    os.symlink(package_path + "/pygments-lexer-overrides/templates.py",  candidate + "/templates.py")
    os.symlink(package_path + "/pygments-lexer-overrides/css.py",  candidate + "/css.py")
except OSError as e:
    print ("Could not create a symbolic link to " + e.filename + ". " + e.strerror)
    sys.exit(-3)

print("Finished installing the customized pygments lexers!")
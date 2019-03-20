from gherkan.flask_api import gherkan_rest
import sys


if __name__ == "__main__":
    print("calling via main")
    args = sys.argv[1:] if len(sys.argv) > 1 else None
    gherkan_rest.main(args)
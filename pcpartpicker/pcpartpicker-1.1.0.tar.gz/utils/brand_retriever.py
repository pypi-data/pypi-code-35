from pcpartpicker import API
from utils.tries import get_brands


def main():
    api = API()
    part_data = api.retrieve_all()
    brands = get_brands(part_data)
    print(brands)


if __name__ == "__main__":
    main()

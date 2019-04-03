from simplepass.simple import main, get_version


if __name__ == '__main__':
    if get_version():
        main()
    else:
        print('You need to be on Python 3.0 or greater to run SimplePass.')

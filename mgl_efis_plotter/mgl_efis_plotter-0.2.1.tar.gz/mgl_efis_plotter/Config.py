class Config:
    units = {
        'airspeed': 'knots',  # 'knots' or 'kph'
        'barometer': 'hg',  # 'hg' or 'millibars'
        'fuel': 'gallons',  # 'gallons' or 'liters'
        'manifoldPressure': 'hg',  # 'hg' or 'millibars'
        'oilPressure': 'psi',  # 'psi' or 'millibars'
        'ambientTemperature': 'c',  # 'f' or 'c'
        'engineTemperature': 'f',  # 'f' or 'c'
    }

    # set each thermocouple value to one of 'cht' or 'egt' or None (capitalized and without quotation marks)
    # the values that you set here must match the configuration of your RDAC
    thermocouples = {
        1: 'cht',
        2: 'egt',
        3: 'cht',
        4: 'egt',
        5: 'cht',
        6: 'egt',
        7: 'cht',
        8: 'egt',
        9: None,
        10: None,
        11: None,
        12: None,
    }

    plot_dimensions = (12, 8)  # width & height in inches
    plot_dpi = 100  # dots per inch
    plot_font_size = 14

    rolling_window = 16  # bigger numbers make smoother graphs; start with 16

    # iEFIS seems to add about 260 seconds to the timestamp at the top of the hour
    new_flight_delta = 300

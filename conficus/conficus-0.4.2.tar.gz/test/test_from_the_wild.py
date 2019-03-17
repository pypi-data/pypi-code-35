import conficus


def test_wild_multiline_sql(cfg_pth):

    lines = conficus.read_config(str(cfg_pth['wilderness']))
    config = conficus._parse(lines)

    value = config['config.sequence_po_sql']

    assert value.multiline is True
    assert len(value.raw_value) == 9
    assert value.raw_value[8].startswith('FFD.')


def test_sequence_with_strings_containing_commas(cfg_pth):
    lines = conficus.read_config(str(cfg_pth['wilderness']))
    config = conficus._parse(lines)

    value = config['config.parser']

    assert value.multiline is False
    assert value.value == r'(0,1,"^\d{10,14}$")'

    config = conficus._coerce(config)
    value = config['config.parser']
    assert value == (0, 1, r"^\d{10,14}$")
    assert len(value) == 3
    assert value[2] == r"^\d{10,14}$"

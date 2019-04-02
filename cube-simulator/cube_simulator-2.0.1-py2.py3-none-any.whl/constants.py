__author__ = 'SHASHANK'

BANK_HOLIDAYS = ['2019-01-26', '2019-04-01', '2019-04-19', '2019-06-05',
                 '2019-08-12', '2019-08-15', '2019-09-10', '2019-10-02',
                 '2019-10-08', '2019-12-25']


BSE_HOLIDAYS = ['2019-03-04', '2019-03-21', '2019-04-17', '2019-04-19',
                '2019-05-01', '2019-06-05', '2019-08-12', '2019-08-15',
                '2019-09-02', '2019-09-10', '2019-10-02', '2019-10-08',
                '2019-10-28', '2019-11-12', '2019-12-25']

SCHEME_HOLIDAYS = {
    "EDGCGP-GR": [
        '2019-01-01', '2019-02-07', '2019-04-05', '2019-04-22', '2019-05-13', '2019-06-07',
        '2019-07-01', '2019-10-01', '2019-10-07', '2019-12-24', '2019-12-26', '2019-12-31']
}

MF_ALLOTMENT_TAT = {
    'Default': [1, 1],
    'F309-GR': [1, 2],
    '410-GR': [1, 2],
    'RELLFTPI-GR': [2, 0],
    'RGFEF-GR': [1, 1],
    'AXFXS153-GR': [1, 1],
    'EDGCGP-GR': [1, 1],
    'CPGP-GR': [1, 1],
    'CREQGP-GR': [1, 1],
    'RELRSFB-GR': [1, 1]
}


MF_REDEMPTION_TAT = {
    1: ['UTICPIGG-GR', 'UTIFLOTNG-GR', 'UTISTINCME-GR', 'RELLFTPI-GR', 'RGF-MTGP-GR','FT406-GR', 'ICICI1565-GR',
        'IIFLLRG-GR', 'DSP52-GR', 'K252-GR', 'K462-GR', 'LT154L-GR', 'LTLCG-GR', 'SBI086G-GR', 'SBI086G-GR-L0',
        'TLSG01-GR', 'TLSG01-GR-L0', 'UTIFLOTNG-GR-L1', 'INLFGP-GR', 'PLFSG-GR', 'F309-GR', 'AXFXS153-GR',
        'ICLNGTEM26PP-GR', 'IDFC280-GR'],
    2: ['UTIMIS-GR-M'],
    5: ['EDGCGP-GR','EDEMGP-GR', 'PEGP-GR', '410-GR', 'PEDP-DP', 'RLJEGP-GR']
}

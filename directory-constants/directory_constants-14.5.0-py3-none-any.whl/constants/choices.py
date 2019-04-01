import json
from operator import itemgetter
import os

from directory_constants.constants import cms, sectors


SPECIFIC = 'specific'
OPEN_ENDED = 'open_ended'
DISTRIBUTION = 'distribution'
WHOLESALE = 'wholesale'
RETAIL = 'retail'
HOSPITALITY = 'hospitality'
CATERING = 'catering'
MANUFACTURING = 'manufacturing'

TYPE_OF_ENQUIRIES = (
    (SPECIFIC, 'Specific'),
    (OPEN_ENDED, 'Open-ended'),
)

FOOD_LEAD_GENERATION_BUSINESS_MODELS = (
    (DISTRIBUTION, 'Distribution'),
    (WHOLESALE, 'Wholesale'),
    (RETAIL, 'Retail'),
)

FOOD_LEAD_GENERATION_SECTORS = (
    (RETAIL, 'Retail'),
    (HOSPITALITY, 'Hospitality'),
    (CATERING, 'Catering'),
    (MANUFACTURING, 'Manufacturing'),
)

LEGAL_LEAD_GENERATION_SECTORS = (
    (sectors.TECHNOLOGY, 'Technology'),
    (sectors.FOOD_AND_DRINK, 'Food and drink'),
    (sectors.RETAIL_AND_LUXURY, 'Retail'),
    (
        sectors.FINANCIAL_AND_PROFESSIONAL_SERVICES,
        (
            'Professional services (for example, financial '
            'services or business consulting'
        )
    ),
    (sectors.MARINE, 'Marine'),
    (sectors.ENERGY, 'Energy'),
)

LEGAL_LEAD_GENERATION_NEED = (
    (
        'General-business-advice-and-partnership',
        'General business advice and partnership'
    ),
    ('Business-start-up-advice', 'Business start-up advice'),
    ('Drafting-of-contracts', 'Drafting of contracts'),
    ('Mergers-and-acquisitions', 'Mergers and acquisitions'),
    ('Immigration', 'Immigration'),
    ('Dispute-resolution', 'Dispute resolution'),
)

LEAD_GENERATION_EXPORT_DESTINATIONS = (
    ('CN', 'China'),
    ('DE', 'Germany'),
    ('IN', 'India'),
    ('JP', 'Japan'),
    ('US', 'United States'),
)

INDUSTRIES = (
    (sectors.AEROSPACE, 'Aerospace'),
    (sectors.ADVANCED_MANUFACTURING, 'Advanced manufacturing'),
    (sectors.AIRPORTS, 'Airports'),
    (
        sectors.AGRICULTURE_HORTICULTURE_AND_FISHERIES,
        'Agriculture, horticulture and fisheries'
    ),
    (sectors.AUTOMOTIVE, 'Automotive'),
    (
        sectors.BIOTECHNOLOGY_AND_PHARMACEUTICALS,
        'Biotechnology and pharmaceuticals'
    ),
    (
        sectors.BUSINESS_AND_CONSUMER_SERVICES,
        'Business and consumer services'
    ),
    (sectors.CHEMICALS, 'Chemicals'),
    (
        sectors.CLOTHING_FOOTWEAR_AND_FASHION,
        'Clothing, footwear and fashion'),
    (sectors.COMMUNICATIONS, 'Communications'),
    (sectors.CONSTRUCTION, 'Construction'),
    (sectors.CREATIVE_AND_MEDIA, 'Creative and media'),
    (sectors.EDUCATION_AND_TRAINING, 'Education and training'),
    (sectors.ELECTRONICS_AND_IT_HARDWARE, 'Electronics and IT hardware'),
    (sectors.ENVIRONMENT, 'Environment'),
    (
        sectors.FINANCIAL_AND_PROFESSIONAL_SERVICES,
        'Financial and professional services'
    ),
    (sectors.FOOD_AND_DRINK, 'Food and drink'),
    (
        sectors.GIFTWARE_JEWELLERY_AND_TABLEWARE,
        'Giftware, jewellery and tableware'
    ),
    (sectors.GLOBAL_SPORTS_INFRASTRUCTURE, 'Global sports infrastructure'),
    (sectors.HEALTHCARE_AND_MEDICAL, 'Healthcare and medical'),
    (
        sectors.HOUSEHOLD_GOODS_FURNITURE_AND_FURNISHINGS,
        'Household goods, furniture and furnishings'
    ),
    (sectors.LIFE_SCIENCES, 'Life sciences'),
    (sectors.LEISURE_AND_TOURISM, 'Leisure and tourism'),
    (sectors.LEGAL_SERVICES, 'Legal services'),
    (sectors.MARINE, 'Marine'),
    (
        sectors.MECHANICAL_ELECTRICAL_AND_PROCESS_ENGINEERING,
        'Mechanical electrical and process engineering'
    ),
    (sectors.METALLURGICAL_PROCESS_PLANT, 'Metallurgical process plant'),
    (
        sectors.METALS_MINERALS_AND_MATERIALS,
        'Metals, minerals and materials'
    ),
    (sectors.MINING, 'Mining'),
    (sectors.OIL_AND_GAS, 'Oil and gas'),
    (sectors.PORTS_AND_LOGISTICS, 'Ports and logistics'),
    (sectors.POWER, 'Power'),
    (sectors.RAILWAYS, 'Railways'),
    (sectors.RENEWABLE_ENERGY, 'Renewable energy'),
    (sectors.RETAIL_AND_LUXURY, 'Retail and luxury'),
    (sectors.SECURITY, 'Security'),
    (
        sectors.SOFTWARE_AND_COMPUTER_SERVICES,
        'Software and computer services'
    ),
    (
        sectors.TEXTILES_INTERIOR_TEXTILES_AND_CARPETS,
        'Textiles, interior textiles and carpets'
    ),
    (sectors.WATER, 'Water'),
)

EMPLOYEES = (
    ('1-10', '1-10'),
    ('11-50', '11-50'),
    ('51-200', '51-200'),
    ('201-500', '201-500'),
    ('501-1000', '501-1,000'),
    ('1001-10000', '1,001-10,000'),
    ('10001+', '10,001+'),
)

CONTACT_OPTIONS = (
    ('EMAIL', 'Email'),
    ('PHONE', 'Phone'),
)


CMS_APP_CHOICES = [
    (cms.FIND_A_SUPPLIER, 'Find a Supplier'),
    (cms.EXPORT_READINESS, 'Export Readiness'),
    (cms.INVEST, 'Invest'),
    (cms.COMPONENTS, 'Components'),
    (cms.GREAT_INTERNATIONAL, 'Great International')
]


# from https://www.registers.service.gov.uk/registers/country
country_fixture_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '../fixtures/country.json'
)
with open(country_fixture_path, 'r') as f:
    COUNTRY_CHOICES = []
    for country in json.loads(f.read()).values():
        for item in country['item']:
            if 'end-date' not in item:
                COUNTRY_CHOICES.append((item['country'], item['name']))
    COUNTRY_CHOICES.sort(key=itemgetter(1))


EU_COUNTRIES = {
    'AT': 'Austria',
    'BE': 'Belgium',
    'BG': 'Bulgaria',
    'HR': 'Croatia',
    'CY': 'Cyprus',
    'CZ': 'Czechia',
    'DK': 'Denmark',
    'EE': 'Estonia',
    'FI': 'Finland',
    'FR': 'France',
    'DE': 'Germany',
    'GR': 'Greece',
    'HU': 'Hungary',
    'IE': 'Ireland',
    'IT': 'Italy',
    'LV': 'Latvia',
    'LT': 'Lithuania',
    'LU': 'Luxembourg',
    'MT': 'Malta',
    'NL': 'Netherlands',
    'PL': 'Poland',
    'PT': 'Portugal',
    'RO': 'Romania',
    'SK': 'Slovakia',
    'SI': 'Slovenia',
    'ES': 'Spain',
    'SE': 'Sweden'
}

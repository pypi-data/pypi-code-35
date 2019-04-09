# -*- coding: utf-8 -*-

BASE_URL = 'https://play.google.com/store/apps'
SUGGESTION_URL = 'https://market.android.com/suggest/SuggRequest'
SEARCH_URL = 'https://play.google.com/store/search'
SEARCH_PAGINATED_URL = 'https://play.google.com/store/apps/collection/search_results_cluster_apps?gsr={gsr}&authuser=0'

CONCURRENT_REQUESTS = 10
USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
              'AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/45.0.2454.101 Safari/537.36')

# Number of results to retrieve from a collection. Range(1 - 120)
NUM_RESULTS = 120

# Number of results to retrieve from a developer
DEV_RESULTS = 24

# Number of results to retrieve from similar. Range (1 - 60)
SIMILAR_RESULTS = 24

# Number of results to retrieve from search and max page possible
SEARCH_RESULTS = 48
SEARCH_MAX_PAGE = 5

# pagTok post data strings to paginate through search results
PAGE_TOKENS = (
    '-p6BnQMCCDE=:S:ANO1ljJ4Cw8',
    '-p6BnQMCCGI=:S:ANO1ljJYYFs',
    '-p6BnQMDCJMB:S:ANO1ljLvbuA',
    '-p6BnQMDCMQB:S:ANO1ljIeRbo',
    '-p6BnQMDCPUB:S:ANO1ljKG00U'
)

UNWANTED_KEYS = (
    'description_html',
    'screenshots',
    'video',
    'histogram',
    'interactive_elements',
    'recent_changes'
)

# Regex to find page tokens within scrip tags
TOKEN_RE = r'GAEiA[\w=]{3,7}:S:ANO1lj[\w]{5}'

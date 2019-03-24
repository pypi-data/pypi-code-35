from typing import Dict, List, Set

import tweepy
from tweepy import Status

from twitter_fire_scraper.twitter import TwitterAuthentication
from twitter_fire_scraper.util import merge_status_dict


class Scraper:

    def __init__(self, twitter_authentication=None):
        # type: (Scraper, TwitterAuthentication) -> None

        # They did not pass in any authentication. Attempt to auto-detect it.
        if not twitter_authentication:
            self.twitter_authentication = TwitterAuthentication.autodetect_twitter_auth()
        else:  # They passed us a TwitterAuthentication object
            self.twitter_authentication = twitter_authentication

        # Tweepy API object. Can make API calls.
        self.api = tweepy.API(self.twitter_authentication.oauth_handler,
                              wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        # Default amount of tweets to retrieve.
        self.default_count = 10

        # Default accounts to scrape.
        # self.accounts = accounts in data/TwitterAccounts.yml

    def scrape_terms(self, terms, count=None, geocode=None):
        # type: (Scraper, Set[str], int, str) -> Dict[str, List[Status]]
        """
        Term-scraping method. Can scrape a set of terms.

        A term is either a hashtag or a piece of text.

        :param geocode: Geographical area to search in. Can be blank.
        :param terms:  List of terms to search for.
        :param count: Maximum tweets to return per search term.
        :return: A dictionary containing {'search-term': List[Status]} pairs.
        """

        if not count:
            count = self.default_count

        results = {}  # type: Dict[str, List[Status]]

        # For each search term,
        for search_term in terms:

            # Make a cursor that can get tweets.
            cursor = tweepy.Cursor(self.api.search, q=search_term, geocode=geocode)

            # For each result of a search term,
            for status in cursor.items(count):  # type: Status

                if search_term not in results:
                    results[search_term] = list()

                # Add the status to a particular search term.
                results[search_term].append(status)

        return results

    def scrape_accounts(self, accounts, count=None):
        # type: (Scraper, Set[str], int) -> Dict[str, List[Status]]
        """
        Account-scraping method. Can scrape a set of accounts.

        An account is either a screenname or @screenname, i.e. both 'Dude123' and '@Dude123' are valid.

        :param accounts: List of accounts to search in.
        :param count: Maximum tweets to return per account.
        :return: A dictionary containing {'@Dude123': List[Status]} pairs.
        """

        if not count:
            count = self.default_count

        results = dict()

        for account in accounts:
            statuses = self.api.user_timeline(screen_name=account, count=count)

            if account not in results:
                results[account] = list()

            for status in statuses:
                results[account].append(status)

        return results

    def scrape(self, terms=None, accounts=None, count=None, geocode=None):
        # type: (Scraper, Set[str], Set[str], int, str) -> Dict[str, List[Status]]
        """
        General-purpose scraping method. Can scrape search terms, and accounts.

        :param geocode: Geographical area to search in. Can be blank.
        :param terms:  List of terms to search for.
        :param accounts: List of account names to search.
        :param count: Maximum tweets to return per search term.
        :return: A dictionary containing {'search-term': List[Status]} pairs.

        Examples:
            >>> scrape(geocode="41.8297855,-87.666775,50mi", terms={"pizza", "waffles"}, maximum=3)
            {'pizza': {Status, Status, Status},
            'waffles': {Status, Status}}
        """
        if not count:
            count = self.default_count

        if (not terms) and (not accounts):
            raise ValueError("No terms or accounts specified.")

        results = dict()

        if terms:
            terms_results = self.scrape_terms(terms=terms, count=count, geocode=geocode)

            results = merge_status_dict(results, terms_results)

        if accounts:
            accounts_results = self.scrape_accounts(accounts=accounts, count=count)

            results = merge_status_dict(results, accounts_results)

        return results

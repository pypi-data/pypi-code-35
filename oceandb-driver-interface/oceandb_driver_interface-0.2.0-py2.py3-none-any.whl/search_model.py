#  Copyright 2018 Ocean Protocol Foundation
#  SPDX-License-Identifier: Apache-2.0


class QueryModel(object):
    def __init__(self, query=None, sort: dict = None, offset=100, page=1):
        assert page >= 1, f'Invalid page value {page}. Required page >= 1.'
        self.query = query
        self.sort = sort
        self.offset = offset
        self.page = page


class FullTextModel(object):
    def __init__(self, text=None, sort: dict = None, offset=100, page=1):
        assert page >= 1, f'Invalid page value {page}. Required page >= 1.'
        self.text = text
        self.sort = sort
        self.offset = offset
        self.page = page

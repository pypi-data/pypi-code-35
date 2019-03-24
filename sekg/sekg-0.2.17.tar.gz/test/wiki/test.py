from sekg.wiki.search_domain_wiki.search import get_wd_by_title

if __name__ == '__main__':
    max_candidate_num = 1
    title = "maximum length"
    wd = get_wd_by_title(title, use_proxies=True, max_candidate_num=1)
    if wd:
        print(wd)

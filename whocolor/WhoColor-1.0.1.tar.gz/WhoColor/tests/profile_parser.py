import pickle
import cProfile
import pstats
import io

from WhoColor.parser import WikiMarkupParser


def profile_parser(test_data_file):
    """
    Test data file is a pickle file which contains a dictionary with rev text and tokens.
    """
    with open(test_data_file, 'rb') as f:
        test_data = pickle.load(f)
    # shrinked datasets - to check the validity quickly and fix the bugs
    # test_data = pickle.load(open('who_color_test_data_shrinked.p','rb'))

    pr = cProfile.Profile()
    pr.enable()

    print('Profiling the WhoColor parser')
    for article, data in test_data.items():
        print(article)
        p = WikiMarkupParser(data['rev_text'], data['tokens'])
        # cProfile.run('p.generate_extended_wiki_markup()')
        # break
        p.generate_extended_wiki_markup()

    pr.disable()

    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

    # save the content into a file and

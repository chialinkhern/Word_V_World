import pickle

from word_v_world.query_ww2cf import get_descriptives, query_by_key, query_by_value
from word_v_world import config

# TODO - get query by value working
# TODO - make more efficient re: memory usage

# load in combined_ww2cf pickle
# combined_ww2cf_path = config.LocalDirs.root / 'data' / 'combined_ww2cf.pkl'
# combined_ww2cf = pickle.load(combined_ww2cf_path.open('rb'))


# create a test dictionary for debugging
test_dict = {("hello", "mother"): 99,
             ("hi", "mom"): 1000,
             ("happy", "thanksgiving"): 1}


def main():
    # query_by_key(combined_ww2cf)
    query_by_value(test_dict)
    # get_descriptives(combined_ww2cf)


main()

# Created by Zack on 9/25/2017.
# Translated into Python on 3/13/2019


# 	@Override
# 	public <I, C extends Collection<? extends I>> boolean anySatisfy(C items, TGMatcher<I> matcher) {
# 		for (I item : items) {
# 			if (matcher.isMatch(item)) {
# 				return true;
# 			}
# 		}
# 		return false;
# 	}
# 	@Override
# 	public <T> T coalesce(T primary, T alternate) {
# 		return primary != null ? primary : alternate;
# 	}
# 	@Override
# 	public <I, O, IC extends Collection<? extends I>> List<O> collect(IC items, TGMatcher<I> matcher, TGTransformer<I, O> transformer) {
# 		List<O> results = new ArrayList<>(items.size());
# 		for (I item : items) {
# 			if (matcher.isMatch(item)) {
# 				results.add(transformer.transform(item));
# 			}
# 		}
# 		return results;
# 	}
# 	@Override
# 	public <I, C extends Collection<? extends I>> int count(C items, TGMatcher<I> matcher) {
# 		int count = 0;
# 		for (I item : items) {
# 			if (matcher.isMatch(item)) {
# 				count++;
# 			}
# 		}
# 		return count;
# 	}
# 	@Override
# 	public <S, I extends TGApplicability<S>, C extends Collection<I>> I detectFirstApplicable(C items, S situation,
#                                                                                             I defaultItem) {
# 		for (I item : items) {
# 			if (item.isApplicable((situation))) {
# 				return item;
# 			}
# 		}
# 		return defaultItem;
# 	}
# 	public <I> I firstItem(Collection<I> items, I defaultItem) {
# 		return isNotEmpty(items) ? items.iterator().next() : defaultItem;
# 	}
#
# 	@Override
# 	public <I, C extends Collection<? extends I>> I firstMatch(C items, TGMatcher<I> matcher, I defaultItem) {
# 		for (I item : items) {
# 			if (matcher.isMatch(item)) {
# 				return item;
# 			}
# 		}
# 		return defaultItem;
# 	}

# 	protected boolean isNotEmpty(Collection<?> items) {
# 		return items != null && items.size() > 0;
# 	}

# 	@Override
# 	public <I, C extends Collection<? extends I>> boolean noneSatisfy(C items, TGMatcher<I> matcher) {
# 		return !anySatisfy(items, matcher);
# 	}

# 	@Override
# 	public <I> I randomItem(List<I> items) {
# 		int index = random.nextInt(items.size());
# 		return items.get(index);
# 	}
# NOTE: Replaced by random.sample(list, 1)
# 	@Override
# 	public <I, C extends Collection<? extends I>> void reactToEach(C items, TGReaction<I> reaction) {
# 		for (I item : items) {
# 			reaction.reactTo(item);
# 		}
# 	}

# 	@Override
# 	public <I, C extends Collection<? extends I>> void reactToFirstMatch(C items, TGMatcher<I> matcher,
#                                                                        TGReaction<I> reaction,
#                                                                        TGExecutable onNoMatch) {
# 		for (I item : items) {
# 			if (matcher.isMatch(item)) {
# 				reaction.reactTo(item);
# 				return;
# 			}
# 		}
# 		onNoMatch.execute();
# 	}

# 	@Override
# 	public <I, C extends Collection<? extends I>> void reactToMatches(C items, TGMatcher<I> matcher,
#                                                                     TGReaction<I> reaction) {
# 		for (I item : items) {
# 			if (matcher.isMatch(item)) {
# 				reaction.reactTo(item);
# 			}
# 		}
# 	}

# 	@Override
# 	public <I, IC extends Collection<? extends I>> List<I> reject(IC items, TGMatcher<? super I> matcher) {
# 		List<I> results = new ArrayList<>();
# 		for (I item : items) {
# 			if (!matcher.isMatch(item)) {
# 				results.add(item);
# 			}
# 		}
# 		return results;
# 	}

from patterns.do_nothing_executable import DEFAULT as DO_NOTHING
# 	@Override
# 	public <I, IC extends Collection<? extends I>> List<I> select(IC items, TGMatcher<? super I> matcher) {
# 		List<I> results = new ArrayList<>();
# 		for (I item : items) {
# 			if (matcher.isMatch(item)) {
# 				results.add(item);
# 			}
# 		}
# 		return results;
# 	}
# }
from .abstract_enumerator import TGEnumerator


class TGBasicEnumerator(TGEnumerator):
    def any_satisfy(self, items, matcher):
        for item in items:
            if matcher.is_match(item):
                return True
        return False

    def coalesce(self, primary, alternate):
        return primary if primary is not None else alternate

    def collect(self, items, matcher, transformer):
        results = []
        for item in items:
            if matcher.is_match(item):
                results.append(transformer.transform(item))
        return results

    def count(self, items, matcher):
        count = 0
        for item in items:
            if matcher.is_match(item):
                count += 1
        return count

    def detect_first_applicable(self, items, situation, default_item):
        for item in items:
            if item.is_applicable(situation):
                return item
        return default_item

    def first_item(self, items, default_item):
        return next(iter(items)) if self.is_not_empty(items) else default_item

    def first_match(self, items, matcher, default_item):
        for item in items:
            if matcher.is_match(item):
                return item
        return default_item

    @staticmethod
    def is_not_empty(items):
        return items is not None and len(items) > 0

    def none_satisfy(self, items, matcher):
        return not self.any_satisfy(items, matcher)

    def react_to_each(self, items, reaction):
        for item in items:
            reaction.react_to(item)

    def react_to_first_match(self, items, matcher, reaction, on_no_match=DO_NOTHING):
        for item in items:
            if matcher.is_match(item):
                reaction.react_to(item)
                return
        on_no_match.execute()

    def react_to_matches(self, items, matcher, reaction):
        for item in items:
            if matcher.is_match(item):
                reaction.react_to(item)

    def reject(self, items, matcher):
        results = []
        for item in items:
            if not matcher.is_match(item):
                results.append(item)
        return results

    def select(self, items, matcher):
        results = []
        for item in items:
            if matcher.is_match(item):
                results.append(item)
        return results


# 	public static final TGEnumerator DEFAULT = new TGBasicEnumerator();
# 	protected static final TGDoNothingExecutable DO_NOTHING = TGDoNothingExecutable.DEFAULT;
# 	private final Random random = new Random(); # Replaced with random.random
DEFAULT = TGBasicEnumerator()

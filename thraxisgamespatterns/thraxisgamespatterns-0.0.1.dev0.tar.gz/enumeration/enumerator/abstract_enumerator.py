from abc import ABC, abstractmethod


##
# Created by Zack on 9/25/2017.
# Translated into Python on 3/13/2019
#

class TGEnumerator(ABC):

    # Answer whether at least one of the supplied items matches a condition.
    #
    # @param items that might match the condition, must not be null
    # @param matcher the condition to match, must not be null
    # @return true/false
    # <I, C extends Collection<? extends I>> boolean anySatisfy(C items, TGMatcher<I> matcher);

    @abstractmethod
    def any_satisfy(self, items, matcher):
        pass

    # Return the first non null parameter, if no parameters are non null then
    # null will be returned.
    # <p>
    # The name coalesce is used for the same operation in some databases like
    # oracle.
    #
    # @param <T> the type of data being coalesced
    # @param primary will be returned if not null
    # @param alternate to use if primary is null
    # @return primary or alternate, may be null
    # <T> T coalesce(T primary, T alternate);

    @abstractmethod
    def coalesce(self, primary, alternate):
        pass

    # Gather a list of transformed elements that match a supplied criteria.
    #
    # @param items all items that may be transformed
    # @param criteria filters out the items to transform
    # @param transformer converts the items to the desired form
    # @return a collection of transformed items
    # <I, O, IC extends Collection<? extends I>> List<O> collect(IC items, TGMatcher<I> criteria,
    # TGTransformer<I, O> transformer);
    @abstractmethod
    def collect(self, items, matcher, transformer):
        pass

        # Answer a count of the supplied items that match the provided condition.

    #
    # @param items that might match the condition, must not be null
    # @param matcher the condition to match, must not be null
    # @return count of matches
    # <I, C extends Collection<? extends I>> int count(C items, TGMatcher<I> matcher);
    @abstractmethod
    def count(self, items, matcher):
        pass

    # Answer the first item that applies, or default item if none apply.
    #
    # @param items a collection of items that might apply to a situation
    # @param situation the context to which an item may apply
    # @param defaultItem returned if no other items match
    # @return first matching item or defaultItem
    # <S, I extends TGApplicability<S>, C extends Collection<I>> I detectFirstApplicable(C items, S situation,
    # I defaultItem);
    @abstractmethod
    def detect_first_applicable(self, items, situation, default_item):
        pass

    # Get the first element from the supplied collection. Return the default
    # item if the collection is empty.
    #
    # @param items may be null or have no child
    # @param defaultItem the child item when items object is empty
    # @return the first of the elements in the collection
    # <I> I firstItem(Collection<I> items, I defaultItem);
    @abstractmethod
    def first_item(self, items, default_item):
        pass

    # Answer the first item in the list that satisfies the supplied match
    # condition, or the default item if there are no matches.
    #
    # @param items that might match the condition, must not be null
    # @param matcher the condition to match, must not be null
    # @param defaultItem to use if none match
    # @return an item or the default item
    # <I, C extends Collection<? extends I>> I firstMatch(C items, TGMatcher<I> matcher, I defaultItem);
    @abstractmethod
    def first_match(self, items, matcher, default_item):
        pass

    # Answer whether none of the supplied items matches a condition. <br>
    # If items is empty then true is returned.
    #
    # @param items that might match the condition, must not be null
    # @param matcher encapsulates the condition(s) to match, must not be null
    # @return true/false
    # <I, C extends Collection<? extends I>> boolean noneSatisfy(C items, TGMatcher<I> matcher);
    @abstractmethod
    def none_satisfy(self, items, matcher):
        pass

    # Get an arbitrary element from the supplied collection.
    # <p>
    # If the collection is empty an exception will be thrown.
    #
    # @param items must have at least one element
    # @return one of the elements in the collection
    # <I> I randomItem(List<I> items);
    # NOTE: Replaced by random.sample(list, 1)

    # Iterate through the supplied items and perform an action on the all
    # items.
    #
    # @param items that need the same reaction, must not be null
    # @param reaction to the items, must not be null
    # <I, C extends Collection<? extends I>> void reactToEach(C items, TGReaction<I> reaction);
    @abstractmethod
    def react_to_each(self, items, reaction):
        pass

    # Iterate through the supplied items and perform an action on the earliest
    # item that meets the criteria. If none of the items meet the criteria then
    # function will simply return.
    #
    # @param items that might match the condition, must not be null
    # @param matcher the condition to match, must not be null
    # @param reaction to the first item that matches, must not be null
    # <I, C extends Collection<? extends I>> void reactToFirstMatch(C items, TGMatcher<I> matcher,
    # TGReaction<I> reaction);
    # Iterate through the supplied items and perform an action on the earliest
    # item that meets the criteria. If none of the items meet the criteria then
    # the supplied onNoMatch action will be performed.
    #
    # @param items that might match the condition, must not be null
    # @param matcher the condition to match, must not be null
    # @param reaction to the first item that matches, must not be null
    # @param onNoMatch executable to perform when non of the items match
    # <I, C extends Collection<? extends I>> void reactToFirstMatch(C items, TGMatcher<I> matcher,
    # TGReaction<I> reaction, TGExecutable onNoMatch);
    @abstractmethod
    def react_to_first_match(self, items, matcher, reaction, on_no_match):
        pass

    # Iterate through the supplied items and perform an action on the all items
    # that meets the criteria. If none of the items meet the criteria then
    # function will simply return.
    #
    # @param items that might match the condition, must not be null
    # @param matcher the condition to match, must not be null
    # @param reaction to the items that matches, must not be null
    # <I, C extends Collection<? extends I>> void reactToMatches(C items, TGMatcher<I> matcher, TGReaction<I> reaction);
    @abstractmethod
    def react_to_matches(self, items, matcher, reaction):
        pass

    # Gather a list of elements that does not match a supplied criteria.
    #
    # @param items to be filtered
    # @param matcher filters the items
    # @return a collection of items that not satisfy the matcher
    # <I, IC extends Collection<? extends I>> List<I> reject(IC items, TGMatcher<? super I> matcher);
    @abstractmethod
    def reject(self, items, matcher):
        pass

    # Gather a list of elements that match a supplied criteria.
    #
    # @param items to be filtered
    # @param matcher filters the items
    # @return a collection of items that satisfy the matcher
    # <I, IC extends Collection<? extends I>> List<I> select(IC items, TGMatcher<? super I> matcher);
    @abstractmethod
    def select(self, items, matcher):
        pass

# package com.games.thraxis.framework.transforming;
#
# import java.util.ArrayList;
# import java.util.Collection;
# import java.util.List;
#
# import android.support.annotation.NonNull;
#
# import com.games.thraxis.framework.enumeration.enumerator.TGBasicEnumerator;
# import com.games.thraxis.framework.enumeration.enumerator.TGEnumerator;
# import com.games.thraxis.framework.enumeration.matcher.TGMatcher;
#
# /##
#  # Created by Zack on 9/25/2017.
#  #/
#
# public abstract class TGBaseTransformer<O, T> implements TGTransformer<O, T> {
#
# 	private final TGEnumerator enumerator = TGBasicEnumerator.DEFAULT;
#
# 	protected void addNonBlank(Collection<String> strings, String string) {
# 		String trimmed = ensureNotNull(string).trim();
# 		if (trimmed.length() > 0) {
# 			strings.add(trimmed);
# 		}
# 	}
#
# 	protected <I, C extends Collection<? extends I>> boolean anySatisfy(C items, TGMatcher<I> matcher) {
# 		return enumerator.anySatisfy(items, matcher);
# 	}
#
# 	protected String coalesce(String primary, String alternate) {
# 		return enumerator.coalesce(primary, alternate);
# 	}
#
# 	protected abstract T convert(O original);
#
# 	protected T defaultTransformation() {
# 		return null;
# 	}
#
# 	protected String ensureNotNull(String value) {
# 		return coalesce(value, "");
# 	}
#
# 	protected <I> I firstItem(Collection<I> items, I defaultItem) {
# 		return enumerator.firstItem(items, defaultItem);
# 	}
#
# 	protected <I> I firstMatch(@NonNull Collection<I> items, @NonNull TGMatcher<I> matcher, I defaultItem) {
# 		return enumerator.firstMatch(items, matcher, defaultItem);
# 	}
#
# 	protected <I, IC extends Collection<? extends I>> List<I> select(IC items, TGMatcher<? super I> matcher) {
# 		return enumerator.select(items, matcher);
# 	}
#
# 	@Override
# 	public final T transform(O original) {
# 		return original == null ? defaultTransformation() : convert(original);
# 	}
#
# 	@Override
# 	public List<T> transformAll(Collection<O> inItems) {
# 		List<T> outItems = new ArrayList<>(inItems.size());
# 		transformAll(inItems, outItems);
# 		return outItems;
# 	}
#
# 	@Override
# 	public void transformAll(Collection<O> inItems, Collection<T> outItems) {
# 		if (inItems != null) {
# 			transformCollection(inItems, outItems);
# 		}
# 	}
#
# 	@Override
# 	public void transformAll(O[] inItems, Collection<T> outItems) {
# 		if (inItems != null) {
# 			transformArray(inItems, outItems);
# 		}
# 	}
#
# 	protected void transformArray(O[] inItems, Collection<T> outItems) {
# 		for (O inItem : inItems) {
# 			T outItem = transform(inItem);
# 			outItems.add(outItem);
# 		}
# 	}
#
# 	protected void transformCollection(Collection<O> inItems, Collection<T> outItems) {
# 		outItems.clear();
# 		for (O inItem : inItems) {
# 			T outItem = transform(inItem);
# 			outItems.add(outItem);
# 		}
# 	}
# }
from abc import ABC, abstractmethod

from enumeration.enumerator.basic_enumerator import TGBasicEnumerator


class TGAbstractBaseTransformer(ABC):
    def __init__(self):
        self.enumerator = TGBasicEnumerator()

    def add_non_blank(self, strings_list=[], new_string=""):
        string = new_string.strip()
        if self.ensure_not_null(string):
            strings_list.append(string)

    def any_satisfy(self, items, matcher):
        return self.enumerator.any_satisfy(items, matcher)

    def coalesce(self, primary, alternate):
        return self.enumerator.coalesce(primary, alternate)

    @abstractmethod
    def convert(self, original):
        pass

    @staticmethod
    def default_transformation():
        return None

    def ensure_not_null(self, value):
        return self.coalesce(value, "")

    def first_item(self, items, default_item):
        return self.enumerator.first_item(items, default_item)

    def first_match(self, items, matcher, default_item):
        return self.enumerator.first_match(items, matcher, default_item)

    def select(self, items, matcher):
        return self.enumerator.select(items, matcher)

    def transform(self, original):
        return self.default_transformation() if not original else self.convert(original)

    def transform_all(self, items_in, items_out=None):
        if items_out:
            items_out.clear()
        if not items_out:
            items_out = []
        for item in items_in:
            items_out.append(self.transform(item))

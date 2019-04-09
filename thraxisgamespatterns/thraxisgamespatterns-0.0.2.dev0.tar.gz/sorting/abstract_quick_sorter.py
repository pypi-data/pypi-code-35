# package com.games.thraxis.framework.sorting;
#
# import java.util.List;
#
# /##
#  # Created by Zack on 10/19/2017.
#  #/
#
# public abstract class TGQuickSorter<E, C extends Comparable<C>> implements TGSorter<E> {
#
# 	protected void exchange(int i, int j) {
# 		E temp = getValues().get(i);
# 		getValues().set(i, getValues().get(j));
# 		getValues().set(j, temp);
# 	}
#
# 	protected abstract C getComparisonValue(E element);
#
# 	protected E getPivot(int low, int high) {
# 		return getValues().get(low + (high - low) / 2);
# 	}
#
# 	protected abstract List<E> getValues();
#
# 	protected boolean isElementGreaterThan(E element, E pivot) {
# 		return getComparisonValue(element).compareTo(getComparisonValue(pivot)) > 0;
# 	}
#
# 	protected boolean isElementLessThan(E element, E pivot) {
# 		return getComparisonValue(element).compareTo(getComparisonValue(pivot)) < 0;
# 	}
#
# 	protected void quickSort(int low, int high) {
# 		int leftElement = low;
# 		int rightElement = high;
# 		E pivot = getPivot(low, high);
# 		while (leftElement <= rightElement) {
# 			while (isElementLessThan(getValues().get(leftElement), pivot)) {
# 				leftElement++;
# 			}
# 			while (isElementGreaterThan(getValues().get(rightElement), pivot)) {
# 				rightElement--;
# 			}
# 			if (leftElement <= rightElement) {
# 				exchange(leftElement, rightElement);
# 				leftElement++;
# 				rightElement--;
# 			}
# 		}
# 		if (low < rightElement) {
# 			quickSort(low, rightElement);
# 		}
# 		if (leftElement < high) {
# 			quickSort(leftElement, high);
# 		}
# 	}
#
# 	@Override
# 	public List<E> sort() {
# 		if (getValues().size() != 0) {
# 			quickSort(0, getValues().size() - 1);
# 		}
# 		return getValues();
# 	}
# }
from abc import abstractmethod, ABC


class TGAbstractQuickSorter(ABC):
    @abstractmethod
    def get_values(self):
        return []

    def sort(self, array=[]):
        if not array:
            array = self.get_values()
        less = []
        equal = []
        greater = []

        if len(array) > 1:
            pivot = array[0]
            for value in array:
                if value < pivot:
                    less.append(value)
                elif value == pivot:
                    equal.append(value)
                elif value > pivot:
                    greater.append(value)
            # Don't forget to return something!
            return self.sort(less) + equal + self.sort(greater)  # Just use the + operator to join lists
        # Note that you want equal ^^^^^ not pivot
        else:  # You need to handle the part at the end of the recursion - when you only have one element in your array,
            #  just return the array.
            return self.get_values()

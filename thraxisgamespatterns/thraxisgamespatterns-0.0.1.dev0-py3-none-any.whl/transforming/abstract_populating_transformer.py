# package com.games.thraxis.framework.transforming;
#
# import java.util.List;
#
# /##
#  # Created by Zack on 9/25/2017.
#  #/
#
# public abstract class TGPopulatingTransformer<O, T> extends TGBaseTransformer<O, T> implements TGPopulator<O, T> {
#
# 	@Override
# 	protected T convert(O original) {
# 		T target = createTarget();
# 		populate(original, target);
# 		return target;
# 	}
#
# 	protected abstract T createTarget();
#
# 	@Override
# 	protected T defaultTransformation() { return createTarget(); }
#
# 	protected <E> void matchContents(List<E> source, List<E> target){
# 		target.clear();
# 		target.addAll(source);
# 	}
#
# 	@Override
# 	public final void populate(O source, T target){
# 		if (source != null){
# 			populateContents(source, target);
# 		}
# 	}
# 	protected abstract void populateContents(O source, T target);
#
# }
from abc import ABC, abstractmethod


class TGAbstractPopulatingTransformer(ABC):
    def convert(self, original):
        target = self.create_target()
        self.populate(original, target)
        return target

    @abstractmethod
    def create_target(self):
        pass

    def default_transformation(self):
        return self.create_target()

    @staticmethod
    def match_contents(source, target):
        target.clear()
        target.append(source)

    def populate(self, source, target):
        if source:
            self.populate_contents(source, target)

    @abstractmethod
    def populate_contents(self, source, target):
        pass

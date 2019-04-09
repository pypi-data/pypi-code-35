# package com.games.thraxis.framework.transforming;
#
# import java.util.Arrays;
# import java.util.Collection;
# import java.util.HashMap;
# import java.util.Map;
#
# import com.games.thraxis.framework.enumeration.enums.TGRepresentable;
#
# /##
#  # Created by Zack on 9/26/2017.
#  #/
#
# public abstract class TGRepresentableTransformer<T extends TGRepresentable> extends TGBaseTransformer<String, T> {
#
# 	private final Map<String, T> conversionMap;
#
# 	protected TGRepresentableTransformer(Collection<T> knownValues) {
# 		this.conversionMap = createConversionMap(knownValues);
# 	}
#
# 	public TGRepresentableTransformer(Map<String, T> conversionMap) {
# 		this.conversionMap = conversionMap;
# 	}
#
# 	public TGRepresentableTransformer(T[] knownValues) {
# 		this(Arrays.asList(knownValues));
# 	}
#
# 	@Override
# 	protected T convert(String original) {
# 		T entry = conversionMap.get(original);
# 		return entry != null ? entry : convertMissing(original);
# 	}
#
# 	protected T convertMissing(String code) {
# 		String normal = code.trim();
# 		return "".equals((normal)) ? getUnspecifiedTransformation() : createUnrecognizedValue(code);
# 	}
#
# 	protected Map<String, T> createConversionMap(Collection<T> knownValues) {
# 		HashMap<String, T> map = new HashMap<>();
# 		for (T each : knownValues) {
# 			map.put(each.getCode(), each);
# 		}
# 		return map;
# 	}
#
# 	protected abstract T createUnrecognizedValue(String code);
#
# 	@Override
# 	protected final T defaultTransformation() {
# 		return getUnspecifiedTransformation();
# 	}
#
# 	protected abstract T getUnspecifiedTransformation();
# }
from abc import abstractmethod

from enumeration.enums.abstract_representable import TGAbstractRepresentable
from transforming.abstract_base_transformer import TGAbstractBaseTransformer


def create_conversion_map(known_values):
    return_map = {}
    for each in known_values:
        if not isinstance(each, TGAbstractRepresentable):
            raise Exception
        return_map.update({each.get_code(): each})
    return return_map


class TGAbstractRepresentableTransformer(TGAbstractBaseTransformer):
    def __init__(self, known_values=None, conversion_map={}):
        super().__init__()
        self.conversion_map = conversion_map if conversion_map else create_conversion_map(known_values)

    def convert(self, original):
        entry = self.conversion_map.get(original)
        return entry if entry else self.convert_missing(original)

    def convert_missing(self, code):
        normal = code.strip()
        return self.get_unspecified_transformation() if not normal else self.create_unrecognized_value(code)

    @abstractmethod
    def get_unspecified_transformation(self):
        pass

    @abstractmethod
    def create_unrecognized_value(self, code):
        pass

    def default_transformation(self):
        return self.get_unspecified_transformation()

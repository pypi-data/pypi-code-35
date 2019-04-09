# package com.games.thraxis.framework.transforming;
#
# import java.util.Arrays;
# import java.util.Collection;
#
# import com.games.thraxis.framework.enumeration.enums.TGRepresentable;
#
# /##
#  # Created by Zack on 9/26/2017.
#  #/
#
# public class TGBasicRepresentableTransformer<C extends TGRepresentable> extends TGRepresentableTransformer<C> {
#
# 	public static <C extends TGRepresentable> TGTransformer<String, C> newInstance(C[] knownValues, C unknownValue) {
# 		return new TGBasicRepresentableTransformer<>(Arrays.asList(knownValues), unknownValue);
# 	}
#
# 	public static <C extends TGRepresentable> TGTransformer<String, C> newInstance(Collection<C> knownValues,
# 			C unknownValue) {
# 		return new TGBasicRepresentableTransformer<>(knownValues, unknownValue);
# 	}
#
# 	public static <C extends TGRepresentable> TGTransformer<String, C> newInstance(Collection<C> knownValues,
# 			C unrecognizedValue, C unspecifiedValue) {
# 		return new TGBasicRepresentableTransformer<>(knownValues, unrecognizedValue, unspecifiedValue);
# 	}
#
# 	private final C unrecognizedValue;
# 	private final C unspecifiedValue;
#
# 	public TGBasicRepresentableTransformer(Collection<C> knownValues, C unrecognizedValue, C unspecifiedValue) {
# 		super(knownValues);
# 		this.unrecognizedValue = unrecognizedValue;
# 		this.unspecifiedValue = unspecifiedValue;
# 	}
#
# 	public TGBasicRepresentableTransformer(Collection<C> knownValues, C unknownValue) {
# 		this(knownValues, unknownValue, unknownValue);
# 	}
#
# 	@Override
# 	protected C createUnrecognizedValue(String code) {
# 		return unrecognizedValue;
# 	}
#
# 	@Override
# 	protected C getUnspecifiedTransformation() {
# 		return unspecifiedValue;
# 	}
# }
from thraxisgamespatterns.transforming import TGAbstractRepresentableTransformer


def new_instance(known_values, unknown_value, unspecified_value=None):
    return TGBaseRepresentableTransformer(known_values, unknown_value, unspecified_value)


class TGBaseRepresentableTransformer(TGAbstractRepresentableTransformer):
    def __init__(self, known_values, unrecognized_value, unspecified_value=None):
        super().__init__(known_values)
        self.unrecognized_value = unrecognized_value
        self.unspecified_value = unspecified_value if unspecified_value else unrecognized_value

    def create_unrecognized_value(self, code):
        return self.unrecognized_value

    def get_unspecified_transformation(self):
        return self.unspecified_value

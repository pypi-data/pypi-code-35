#
# Created by Zack on 9/26/2017.
# /

# 	public static <E extends TGRepresentable> Map<String, E> createByCodeMap(Collection<E> values, E defaultValue) {
# 		HashMap<String, E> map = new HashMap<>();
# 		for (E each : values) {
# 			map.put(each.getCode(), each);
# 		}
# 		return TGDefaultingMap.withDefault(map, defaultValue);
# 	}
#
# 	public static <E extends TGRepresentable> Map<String, E> createByCodeMap(E[] values, E defaultValue) {
# 		return createByCodeMap(Arrays.asList(values), defaultValue);
# 	}
#
# 	public static <T extends Enum<T>> T fromString(Class<T> enumType, String name, T defaultValue) {
# 		try {
# 			return Enum.valueOf(enumType, name);
# 		} catch (Exception exception) {
# 			return defaultValue;
# 		}
# 	}
# }
# TODO: Determine if this is still required.

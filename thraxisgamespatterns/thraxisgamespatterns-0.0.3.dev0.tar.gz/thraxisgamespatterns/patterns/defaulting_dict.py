# Created by Zack on 9/26/2017.


class TGDefaultingDict(dict):
    def __init__(self, default=None, seq=None, **kwargs):
        super().__init__(seq=seq, **kwargs)
        self.default_value = default

    def get(self, key, **kwargs):
        return super().get(key, **kwargs) if super().get(key, **kwargs) else self.default_value

# public class TGDefaultingMap<K, V> extends TGMapDecorator<K, V> {
#
# 	public static <K, V> TGDefaultingMap<K, V> emptyMap(V defaultValue) {
# 		Map<K, V> emptyMap = Collections.emptyMap();
# 		return new TGDefaultingMap<>(emptyMap, defaultValue);
# 	}
#
# 	public static <K, V> TGDefaultingMap<K, V> withDefault(Map<K, V> map, V defaultValue) {
# 		return new TGDefaultingMap<>(map, defaultValue);
# 	}
#
# 	public static <K, V> TGDefaultingMap<K, V> withDefault(V defaultValue) {
# 		return new TGDefaultingMap<>(new HashMap<K, V>(), defaultValue);
# 	}
#
# 	private V defaultValue;
#
# 	protected TGDefaultingMap(Map<K, V> map) {
# 		super(map);
# 	}
#
# 	public TGDefaultingMap(Map<K, V> map, V defaultValue) {
# 		super(map);
# 		this.defaultValue = defaultValue;
# 	}
#
# 	public V getDefault() {
# 		return defaultValue;
# 	}
#
# 	public void setDefault(V defaultValue) {
# 		this.defaultValue = defaultValue;
# 	}
#
# 	@Override
# 	public String toString() {
# 		return getClass().getSimpleName() + "{defaultValue=" + defaultValue + "," + super.toString() + "}";
# 	}
# }

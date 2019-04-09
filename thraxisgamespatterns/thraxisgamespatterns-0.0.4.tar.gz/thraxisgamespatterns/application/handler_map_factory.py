# package com.games.thraxis.framework.application;
#
# import java.util.HashMap;
# import java.util.Map;
#
# import com.games.thraxis.framework.factories.TGFactory;
#
# /##
#  # Created by Zack on 10/24/2017.
#  #/
#
# public class TGActivityHandlerMapFactory implements TGFactory<Map<String, Class<?>>> {
#
# 	@Override
# 	public Map<String, Class<?>> create() {
# 		Map<String, Class<?>> map = new HashMap<>();
# 		return map;
# 	}
# }
from factories.abstract_factory import TGAbstractFactory


class TGHandlerMapFactory(TGAbstractFactory):
    def create(self, options=None):
        return {}

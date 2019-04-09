# package com.games.thraxis.framework.application;
#
# import android.content.Context;
#
# /##
#  # Created by Zack on 9/26/2017.
#  #/
#
# public class TGBasicContextRegistryLocator implements TGContextRegistryLocator {
#
# 	public static final TGContextRegistryLocator DEFAULT = new TGBasicContextRegistryLocator();
# 	private TGRegistry registry;
#
# 	@Override
# 	public <R extends TGRegistry> R locateRegistry(Context context) {
# 		return (R) registry;
# 	}
#
# 	@Override
# 	public void setRegistry(TGRegistry registry) {
# 		this.registry = registry;
# 	}
# }


class TGBaseContextRegistryLocator:
    def __init__(self):
        self.registry = ""

    def locate_registry(self, context):
        return self.registry


DEFAULT = TGBaseContextRegistryLocator()

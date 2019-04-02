import json

import geojson
import geojsonio
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyproj
import shapely.geometry as shg
import shapely.ops as shops
import shapely.wkb as shwkb
import shapely.wkt as shwkt
from functools import partial
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon

geom_kz=r'POLYGON ((59.501953125 51.39920565355378, 51.50390625 52.50953477032727, 46.40625 50.875311142200765, 45.1318359375 48.516604348867475, 51.37207031249999 41.04621681452063, 56.4697265625 40.713955826286046, 58.00781249999999 44.49650533109348, 68.466796875 40.04443758460856, 80.595703125 41.60722821271717, 85.869140625 46.46813299215554, 89.1650390625 49.009050809382046, 77.2998046875 54.87660665410869, 70.09277343749999 56.07203547180089, 60.1171875 54.316523240258256, 59.501953125 51.39920565355378))'

def remove_redundants(polygons,redundancy_order=2.5,**kwargs):
	area_max=max([g.area for g in polygons])
	candidates=[g for g in polygons]
	for g in list(polygons):
		if np.log10(area_max/g.area)>redundancy_order:
			print('Redundant land is detected. Removing it...')
			candidates.remove(g)
	return candidates

def get_crs(geojson_datum):
	crs_info=geojson_datum.crs.properties['name'].split(':')
	if not crs_info[-1].isnumeric():
		print(crs_info)
		raise NotImplementedError('Could not infer crs. crs_info = \n{}'.format(crs_info))
	return int(crs_info[-1])

def plot_polygon(polygon: shg.Polygon,label=None,ax=None,**kwargs):
	if ax is None: plot=plt.plot
	else: plot=ax.plot
	default_opts=dict(lw=3)
	if label is None: labeler=lambda l:dict(default_opts,label=l)
	else: labeler=lambda l:dict(default_opts,label='{} {}'.format(label,l))
	plotter=lambda linestring,_label:plot(*linestring.xy,**dict(labeler(_label),**kwargs))
	plotter(polygon.exterior,'exterior')
	for i,p_i in enumerate(polygon.interiors):
		plotter(p_i,'interior {}'.format(i))

def plot_poly(p,**kwargs):
	if isinstance(p,shg.MultiPolygon):
		for p in p: plot_poly(p,**kwargs)
	plt.plot(*p.exterior.xy,**kwargs)

def convert_crs(coor_obj,_in: int,_out=4326):
	inproj,outproj=pyproj.Proj(init=f'epsg:{_in}'),pyproj.Proj(init=f'epsg:{_out}')
	converter=lambda xy:np.stack(pyproj.transform(inproj,outproj,*xy),axis=1).reshape(-1,2)
	polygons=list()
	if type(coor_obj) is np.ndarray:
		assert coor_obj.shape[1]==2,\
			"ndarray shape should be (-1,2), but shape={} is provided.".format(coor_obj.shape)
		return converter(np.split(coor_obj,2,axis=1))
	elif type(coor_obj) is shg.Polygon:
		coor_obj=shg.MultiPolygon([coor_obj])
		returner=lambda multipolygon:multipolygon[0]
	elif type(coor_obj) is shg.MultiPolygon:
		returner=lambda multipolygon:multipolygon
		pass
	else: raise NotImplementedError('No implementation for objects of type = {}'.format(type(coor_obj)))
	for g in coor_obj:
		interior_xys=[converter(interior.xy) for interior in g.interiors]
		polygons.append(shg.Polygon(converter(g.exterior.xy),interior_xys))
	return returner(shg.MultiPolygon(polygons))

def reproject_point(point,_in,_out):
	inproj,outproj=pyproj.Proj(init=f'epsg:{_in}'),pyproj.Proj(init=f'epsg:{_out}')
	return shg.Point(pyproj.transform(inproj,outproj,point.x,point.y))

def get_area(geom,in_epsg):
	geom_area=shops.transform(
		partial(
			pyproj.transform,
			pyproj.Proj(init=f'EPSG:{in_epsg}'),
			pyproj.Proj(proj='aea',lat1=geom.bounds[1],lat2=geom.bounds[3])),geom).area
	return geom_area

class SpatialGeom:
	
	@classmethod
	def from_geojson(cls,geojson_datum,crs_in=None,crs_out=4326,**kwargs):
		if isinstance(geojson_datum,str):
			geojson_datum=geojson.load(open(geojson_datum))
		if 'features' in geojson_datum.keys(): geometry=geojson_datum.features[0].geometry
		else: geometry=geojson_datum.geometry
		cad_land=SpatialGeom(shg.shape(geometry),**kwargs)
		if cad_land.geom_obj.is_empty:
			print('Empty entry detected.')
			return cad_land
		cad_land.data['epsg']=crs_out
		if not 'name' in kwargs: cad_land.name=geojson_datum['features'][0]['properties']['KAD_NOMER']
		if crs_in==crs_out: return cad_land
		elif crs_in is None:
			if 'crs' in geojson_datum.keys():
				crs_in=get_crs(geojson_datum)
				if crs_in==crs_out: return cad_land
			elif max(cad_land.geom_obj.bounds)>90:
				#print('Assuming input crs = epsg: 32643')
				#crs_in='epsg:32643'
				raise NotImplementedError(
					'No info to infer from. Please, specify incoming coordinate reference system.')
			else:
				#print('Assuming proper input crs, i.e. "epsg:4326".')
				#return cad_land
				raise NotImplementedError(
					'No info to infer from. Please, specify incoming coordinate reference system.')
		cad_land.convert_crs(crs_in,crs_out)
		return cad_land
	
	def convert_crs(self,_from: int,to=4326):
		if self.geom_obj.is_empty:
			print('Cannot convert empty shape.')
			return self
		if _from==to: return self
		multi_polygon=convert_crs(self.geom_obj,_from,to)
		#if inplace:
		self.geom_obj=multi_polygon
		return self
		# else:
		# 	return SpatialGeom(multi_polygon,redundancy_order=self.redundancy_order,
		# 	                   name=self.name)
		pass
	
	def __init__(self,geom_obj,name=None,**kwargs):
		"""

		:param geom_obj: wkt/wkb string, ndarray or shapely Polygon/Multipolygon
		:param name: name
		:param kwargs:
		redundancy_order = 2.5
		"""
		if isinstance(geom_obj,str):
			try:
				geom_obj=shwkt.loads(geom_obj)
			except Exception as e:
				try:
					json_obj=geojson.loads(geom_obj)
					geom_obj=shg.shape(json_obj['features'][0]['geometry'])
				except Exception as e:
					from shapely import geos
					# geos.WKBWriter.defaults['include_srid']=True
					geom_obj=shwkb.loads(geom_obj,hex=True)
		
		if isinstance(geom_obj,shg.Polygon): geom_obj=shg.MultiPolygon([geom_obj])
		elif isinstance(geom_obj,np.ndarray):
			geom_obj=shg.MultiPolygon([shg.Polygon(geom_obj)])
		self.name=name or 'SpatialGeom'
		self.data=kwargs
		if not geom_obj.is_empty: geom_obj=shg.MultiPolygon(remove_redundants(geom_obj,**kwargs))
		self.geom_obj: shg.MultiPolygon=geom_obj
		self.data['with_holes']=max(self.do_for_each(lambda p:len(list(p.interiors))),default=0)!=0
		pass
	
	def do_for_each(self,func,*args,**kwargs):
		doer=lambda x:func(x,*args,**kwargs)
		#if self.is_multipolygon:
		out=list()
		for p in self.geom_obj:
			out.append(doer(p))
		return out
	
	# else:
	# 	return [doer(self.geom_obj)]
	
	def show_on_geojsonio(self):
		get_displayed=lambda obj:geojsonio.display(json.dumps(shg.mapping(obj)))
		self.do_for_each(get_displayed)
	
	def plot(self,show=False,**kwargs):
		if self.geom_obj.is_empty: return
		# if ax is None: plot=plt.plot
		# else: plot=ax.plot
		# plotter=lambda linearring,label,:plot(*linearring.xy,**dict(dict(label=label),**kwargs))
		#if self.is_multipolygon:
		for i,p in enumerate(self.geom_obj):
			plot_polygon(p,**dict(dict(label='Polygon {}'.format(i)),**kwargs))
		if show:
			plt.legend(loc='best')
			plt.show()
	
	def to_geojson(self,**kwargs):
		return geojson.Feature(geometry=self.geom_obj,**kwargs)
	
	def __bool__(self):
		return self.geom_obj.is_empty
	
	# else:
	# 	plot_polygon(self.geom_obj,'Single polygon',**kwargs)
	
	def get_area(self):
		return get_area(self.geom_obj,4326)
	
	@property
	def box(self):
		return self.geom_obj.envelope.exterior
	
	@property
	def xy(self):
		return np.array(self.geom_obj[0].boundary.xy).T
	
	def __str__(self):
		return '{}: {}'.format(self.name,str(self.geom_obj))

def plot_patches(polygons,ax=None,c=None,**kwargs):
	if ax is None: ax=plt.gca()
	if isinstance(polygons,pd.Series):
		pcol=PatchCollection(polygons.map(lambda p:Polygon(p.exterior)),**kwargs)
	else:
		poly_objs=[Polygon(x.exterior) for x in polygons]
		pcol=PatchCollection(poly_objs,**kwargs)
	if c: pcol.set_color(c)
	ax.add_collection(pcol)

def get_rect(corner,sizes):
	corner=np.array(corner)
	sizes=np.array(sizes)
	return np.array([corner,corner+sizes*(1,0),corner+sizes,corner+sizes*(0,1)])

def get_portion(polygon,offset_ratio,size_ratio):
	p_min=np.array(polygon.bounds[0:2])
	p_max=np.array(polygon.bounds[-2:])
	curr_sizes=(p_max-p_min)
	new_rect=shg.Polygon(get_rect(p_min+curr_sizes*offset_ratio,curr_sizes*size_ratio))
	return new_rect

def get_forecast_region(cad_geom,min_forecast_point_dist=3,forecast_step_degrees=0.25):
	forecast_region=cad_geom.envelope.buffer(min_forecast_point_dist*forecast_step_degrees*1.2)
	return forecast_region.envelope

if __name__=='__main__':
	p=shg.Point(78,43)
	print(reproject_point(p,4326,3857))
	# print(p.x)
	pass

# a1=shg.Polygon(np.random.rand(4,2))
# a2=shg.Polygon()
# b1=shg.MultiPolygon()
# b2=shg.MultiPolygon([a1])
# b3=shg.MultiPolygon([a1,shg.Polygon(np.random.rand(4,2),[np.random.rand(3,2)])])
# c1=SpatialGeom(a1)
# #c2=c1.convert_crs(32642)
# print(convert_crs(np.random.rand(10,2),32642))

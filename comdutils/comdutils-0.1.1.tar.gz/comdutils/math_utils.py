import cv2
import numpy as np 
import random

class LineInspect():
	def __init__(self, image_shape, lines, decay=0.001):
		"""
		a function for Giving the frame (Big Title at the top)
		Args:
			image:				an opencv image with format of BGR
			company_name:		a string, the name of the company
			project_name:       a string, the name of the project
		Return:
			An opencv image
		"""
		self.image_w = image_shape[1]
		self.lines = lines
		self.line_points = []
		# loop over lines
		for i in self.lines:
			m = (i[3] - i[1])/(i[2] - i[0] + decay)
			b = i[1]-(m * i[0])
			# loop over x
			for j in range(self.image_w):
				# check the x limit 
				if j > min(i[0], i[2]) or j < max(i[0], i[2]):
					y = int(m * j + b)
					# check the j limit
					if y > min(i[1], i[3]) and y < max(i[1], i[3]):
						self.line_points.append([j, y])
	
	def is_crossing_line(self, rects, reduce_rect_size=0.3):
		"""
		a function for Giving the frame (Big Title at the top)
		Args:
			image:				an opencv image with format of BGR
			company_name:		a string, the name of the company
			project_name:       a string, the name of the project
		Return:
			An opencv image
		"""
		is_crossing = []
		for i in rects:
			is_point_inside = False
			height = abs(i[3] - i[1])
			xr1 = i[0] 
			xr2 = i[2]
			yr1 = i[1] + (reduce_rect_size * height / 2)
			yr2 = i[3] - (reduce_rect_size * height / 2)
			for j in self.line_points:
				if j[0] > xr1 and j[0] < xr2 and j[1]>yr1 and j[1] < yr2:
					is_point_inside = True
					break
			if is_point_inside:
				is_crossing.append([1, i])
		return is_crossing
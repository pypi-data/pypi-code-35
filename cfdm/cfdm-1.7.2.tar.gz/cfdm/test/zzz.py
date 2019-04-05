import cfdm, numpy, re
q, t = cfdm.read('/home/david/cfdm/docs/_downloads/file.nc')

x = t.constructs
c = t.constructs.filter_by_type('auxiliary_coordinate')
d = c.filter_by_naxes(1)
print 'd=',str(d)
e = d.inverse_filter(1)
print 'e=',str(e)
f = e.inverse_filter(1)
print 'f=',str(f)
g = f.inverse_filter(1)
print 'g=',str(g)
print (repr(x))
print (repr(c))

print (str(e))
print str(f)
print e.__dict__
print f.equals(d)
print g.equals(e)
print g.__dict__
print str(g.inverse_filter())

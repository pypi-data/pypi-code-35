import numpy, masque
from masque.file.gdsii import write, read
from masque.repetition import GridRepetition

p = masque.Pattern(name='hi')
s = masque.Pattern(name='sub')
s.shapes = [masque.shapes.Polygon.rect(lx=10, ly=6, xctr=0, yctr=1)]
g = GridRepetition(pattern=s, a_vector = [100, 0], b_vector = [0, 100], a_count=2, b_count=3, offset=[2,2], rotation=numpy.pi/3)
g2 = GridRepetition(pattern=s, a_vector = [100, 0], b_vector = [0, 100], a_count=2, b_count=3, offset=[-500,-500], rotation=0)
p.subpatterns = [g, g2]

write(p, 'testarr.gds', 1e-9, 1e-3)

pats, _data = read('testarr.gds')

pats['hi'].visualize()

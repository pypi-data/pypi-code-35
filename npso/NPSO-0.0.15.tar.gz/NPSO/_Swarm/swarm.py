import numpy as np
import inspect
from .._Particle.particle import particle
class swarm:
    def __init__(self,function,*args,**kwargs):
        assert hasattr(function,'__call__'),'ERROR: Function input not callable'
        self.function       = function
        self.swarm_size     = kwargs.get('size',100)
        self.tolerance      = kwargs.get('tolerance',0.001)
        self.max_iterations = kwargs.get('iterations',100)


    def __get_dimensions__(self):
        try:
            self.dimensions = len(inspect.getfullargspec(self.function)[0])
        except:
            pass
        return


    def __setup__(self):
        self.particles = [particle(dimensions=self.dimensions) for i
                          in range(self.swarm_size)]
        self.gbest     = float('inf')
        self.gbest_position = np.empty((1,self.dimensions))
        return

    def __update__(self):
        for particle in self.particles:
            contender = self.__fit__(particle)
            particle.current_value = contender
            try:
                particle.history['value'].append(contender)
            except:
                pass
            if particle.pbest_value > contender:
                particle.pbest_value = contender
                particle.pbest_position = particle.position
            if self.gbest > particle.pbest_value:
                self.gbest = particle.pbest_value
                self.gbest_position = particle.pbest_position
                try:
                    self.history['g_best_position'].append(self.gbest_position)
                    self.history['g_best_value'].append(self.gbest)
                except:
                    pass
        return


    def __fit__(self,particle):
        return self.function(*np.split(particle.position,self.dimensions,axis=1))


    def __move__(self):
        c1 = 2.05
        c2 = 2.05
        for particle in self.particles:
            update_velocity = (0.5*particle.pvelocity+c1*np.random.uniform(0,1)*
                              (particle.pbest_position-particle.position)+c2*
                              np.random.uniform(0,1)*(self.gbest_position-
                              particle.position))
            #if self.constriction_factor: #correct

            #    update_velocity = self.__constriction_factor__(c1,c2)*update_velocity
            particle.pvelocity = update_velocity
            particle.move(update_velocity)
        return


    def __record__(self):
        self.history = {'g_best_position': [],
                        'g_best_value'   : []}
        return


    def run(self):
        for i in range(self.max_iterations):
            t1 = self.gbest
            self.__update__()
            t2 = self.gbest
            if t1-t2 < self.tolerance:
                convergence += 1
                change = t1-t2
            elif t1==t2 and change < self.tolerance:
                convergence += 1
            else:
                convergence = 0
            if convergence >= 10:
                print('Optima Obtained from PSO: ',self.gbest)
                print('Location of Optima: ',self.gbest_position)
                print('Converged after ',i,' iterations')
                converged = True
                break
            else:
                converged = False
            try:
                change
            except:
                change = 'not within acceptable range'
            self.__move__()
            self.exit_iteration = i
        if converged == False:
            print('Maximum iterations reached --> 100')
            print('Change -->',change)
            print('Best value obtained: ',self.gbest)
            print('Location of best value: ',self.gbest_position)
        return self.gbest_position,self.gbest


    def summary(self):
        print('====================================')
        print('Particle Swarm Optimization Summary')
        print('====================================')
        print('Swarm Size     |   {0}'.format(self.swarm_size))
        print('Tolerance      |   {0}'.format(self.tolerance))
        print('Max Iterations |   {0}'.format(self.max_iterations))
        print('====================================')
        print('\n')
        return
    def export(self):
        pass
"""
def z(x):
    return x
s = swarm(function=z)
s.summary()
"""

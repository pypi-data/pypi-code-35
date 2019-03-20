# -*- coding: utf-8 -*-
import numpy as np
import numpy.random as nr
import math, time
from copy import deepcopy
import matplotlib.pyplot as plt
np.set_printoptions(threshold=np.inf, precision=8, suppress=True, floatmode='maxprec')





class setting:
    def __init__(self, para_range, score_func, aim, show_pool_func, show_para_func, seed, verbose, **kwargs):
        self.para_range = np.array(para_range)
        self.para_num = len(para_range)
        self.score_func = score_func
        self.aim = aim
        self.show_para_func = show_para_func
        self.show_pool_func = show_pool_func
        nr.seed(seed)
        self.verbose = verbose
        self.kwargs = kwargs
        #self.verbose = verbose
        #self.visible = visible
        #self.maxgen = maxgen
        self.start = time.time()
    
    #set hyper para
    def set_hyper(self, pool_num, parent_num, child_num):
        self.pool_num = pool_num
        self.parent_num = parent_num
        self.child_num = child_num
        #self.rate = rate
    
    #set pool
    def set_pool(self, dtype):
        self.pool, self.pool_score = np.zeros((self.pool_num, self.para_num), dtype=dtype), np.zeros(self.pool_num)
        self.parent, self.parent_score = np.zeros((self.parent_num, self.para_num), dtype=dtype), np.zeros(self.parent_num)
        self.child, self.child_score = np.zeros((self.child_num, self.para_num), dtype=dtype), np.zeros(self.child_num)

    #score pool
    def score_pool(self):        
        for i in range(self.pool_num):
            self.pool_score[i] = self.score_func(self.pool[i], **self.kwargs)
    
    #score child
    def score_child(self):        
        for i in range(self.child_num):
            self.child_score[i] = self.score_func(self.child[i], **self.kwargs)
    
    #save best
    def save_best(self):
        self.best_index = np.argmin(np.abs(self.aim - self.pool_score))
        self.pool_best = deepcopy(self.pool[self.best_index])
        self.pool_score_best = deepcopy(self.pool_score[self.best_index])
        self.pool_score_mean = np.mean(np.abs(self.aim - self.pool_score))
        self.pool_score_mean_save = deepcopy(self.pool_score_mean)

    #save mean
    def save_mean(self):
        self.pool_score_mean = np.mean(np.abs(self.aim - self.pool_score))
        self.pool_score_mean_save = deepcopy(self.pool_score_mean)

    #make parent
    def make_parent(self):
        self.pool_select = nr.choice(range(self.pool_num), self.parent_num, replace = False)
        self.parent = self.pool[self.pool_select]
        self.parent_score = self.pool_score[self.pool_select]

    #make family
    def make_family(self):
        self.family = np.vstack((self.child, self.parent))
        self.family_score = np.hstack((self.child_score, self.parent_score))
    
    #JGG
    def JGG(self):
        #np.argpartition(-array, K)[:K] returns max K index
        #np.argpartition(array, K)[:K] returns min K index
        self.family_select = np.argpartition(np.abs(self.aim - self.family_score), self.parent_num)[:self.parent_num]
        #return to pool
        self.pool[self.pool_select] = self.family[self.family_select]
        self.pool_score[self.pool_select] = self.family_score[self.family_select]
    
    #check and save best
    def check_save_best(self):
        self.best_index_tmp = np.argmin(np.abs(self.aim - self.pool_score))
        if np.abs(self.aim - self.pool_score[self.best_index_tmp]) < np.abs(self.aim - self.pool_score_best):
            #update
            self.best_index = deepcopy(self.best_index_tmp)
            self.pool_best = deepcopy(self.pool[self.best_index])
            self.pool_score_best = deepcopy(self.pool_score[self.best_index])
            return True
        else:
            return False

    #check and save mean
    def check_save_mean(self):
        self.pool_score_mean = np.mean(np.abs(self.aim - self.pool_score))
        if np.abs(self.aim - self.pool_score_mean) < np.abs(self.aim - self.pool_score_mean_save):
            #update
            self.pool_score_mean_save = deepcopy(self.pool_score_mean)
            return True
        else:
            return False

    #print bar
    def print_bar(self, n):
        n0 = int(20*n/(self.maxgen+1)) + 1
        n1 = 20 - n0
        t = time.time() - self.start
        bar = '\r{}% [{}{}] time:{}s gen:{}  φ(□　□;)'.format(str((n*100//self.maxgen)).rjust(3), '#'*n0, ' '*n1, np.round(t, 1), n)
        print(bar, end='')
        #print(bar)
    
    #print bar final
    def print_bar_final(self, n):
        n0 = int(20*n/(self.maxgen+1)) + 1
        n1 = 20 - n0
        t = time.time() - self.start
        bar = '\r{}% [{}{}] time:{}s gen:{}  φ(□　□*)!!'.format(str((n*100//self.maxgen)).rjust(3), '#'*n0, ' '*n1, np.round(t, 1), n)
        #print(bar, end='')
        print(bar)

    def __del__(self):
        pass








class vcopt:
    
    def __init__(self):
        pass

    def __del__(self):
        pass
    
    #2-opt
    def opt2(self, para, score_func, aim, show_para_func=None, seed=None, step_max=float('inf'), **kwargs):
        #
        para, score = np.array(para), score_func(para, **kwargs)
        nr.seed(seed)
        step = 0
        #
        if show_para_func != None:
            kwargs.update({'step_num':step, 'score':round(score, 3)})
            show_para_func(para, **kwargs)
        #opt
        while 1:
            update = False
            if step >= step_max: break
            
            i_set = np.arange(0, len(para)-1)
            nr.shuffle(i_set)
            for i in i_set:
                #continue check
                if update == True: break
                
                j_set = np.arange(i + 1, len(para))
                nr.shuffle(j_set)
                for j in j_set:
                    #continue check
                    if update == True: break
                    
                    #try
                    para_tmp = np.hstack((para[:i], para[i:j+1][::-1], para[j+1:]))
                    score_tmp = score_func(para_tmp, **kwargs)
                    
                    #check and update
                    if np.abs(aim - score_tmp) < np.abs(aim - score):
                        para, score = para_tmp, score_tmp
                        step += 1
                        if show_para_func != None:
                            kwargs.update({'step_num':step, 'score':round(score, 3)})
                            show_para_func(para, **kwargs)
                        update = True
            if update == False:
                break
        return para, score





    #==============================================================#==============================================================
    #==============================================================#==============================================================
    def tspGA(self, para_range, score_func, aim, show_pool_func=None, show_para_func=None, seed=None, verbose=0, **kwargs):#, maxgen=5000):
        #
        tmp = setting(para_range, score_func, aim, show_pool_func, show_para_func, seed, verbose, **kwargs)
        tmp.set_hyper(tmp.para_num*10, 2, 4)
        tmp.set_pool(int)
        
        #3 window
        tmp.window = np.ones((tmp.parent_num, 3), dtype=int)
        #opt2_step
        tmp.opt2_step = tmp.para_num // 2
        if tmp.verbose == 1: tmp.opt2_step = tmp.para_num // 5
        if tmp.verbose == 2: tmp.opt2_step = tmp.para_num // 10
        if tmp.verbose == 3: tmp.opt2_step = tmp.para_num // 20
        
        #gen 1 pool
        for i in range(tmp.pool_num):
            tmp.pool[i,] = deepcopy(tmp.para_range)
            nr.shuffle(tmp.pool[i])
            #mini 2-opt
            tmp.pool[i], tmp.pool_score[i] = self.opt2(tmp.pool[i], tmp.score_func, tmp.aim,\
                                                       step_max=tmp.opt2_step, **tmp.kwargs)
        #
        #tmp.score_pool()
        tmp.save_best()
        tmp.save_mean()
        
        #show
        if tmp.show_pool_func != None:
            tmp.kwargs.update({'gen_num':0, 'best_index':tmp.best_index,\
                               'best_score':round(tmp.pool_score_best, 3),\
                               'mean_score':round(tmp.pool_score_mean + tmp.aim, 3),\
                               'time':round(time.time() - tmp.start, 3)})
            tmp.show_pool_func(tmp.pool, **tmp.kwargs)
        
        #gen 2-
        count = 0
        for n in range(1, 1000000 + 1):
            #
            tmp.make_parent()
            
            #辺に着目したヒュリスティック操作
            #==============================================================
            #ex_parent
            tmp.ex_parent = np.hstack((tmp.parent[:, -1].reshape(tmp.parent_num, 1), tmp.parent, tmp.parent[:, 0].reshape(tmp.parent_num, 1)))            
            #child
            for i in range(tmp.child_num):
                #first para
                s = tmp.para_range[nr.randint(tmp.para_num)]
                tmp.child[i, 0] = s
                #following para
                for j in range(1, tmp.para_num):
                    #the last para index in ex_parent
                    center = np.where(tmp.parent[:]==s)[1] + 1
                    
                    p = np.ones(tmp.para_num) * 0.1
                    for k in range(tmp.parent_num):
                        #3 window
                        tmp.window[k] = tmp.ex_parent[k, center[k] - 1: center[k] + 2]
                        #weight
                        p[tmp.window[k]] += 1.0
                    #mask passed para
                    p[tmp.child[i, 0:j]] = 0.0
                    #choice
                    p *= 1.0 / np.sum(p)
                    s = nr.choice(range(tmp.para_num), p=p)
                    #child
                    tmp.child[i, j] = s
            #==============================================================
            #
            #tmp.score_child()
            tmp.make_family()
            #mini 2-opt
            for i in range(tmp.child_num):
                tmp.family[i], tmp.family_score[i] = self.opt2(tmp.family[i], tmp.score_func, tmp.aim,\
                                                               step_max=tmp.opt2_step, **tmp.kwargs)
            tmp.JGG()
            tmp.check_save_best()
            
            #show
            if n % (tmp.pool_num//2) == 0 and tmp.show_pool_func != None:
                if tmp.show_pool_func != None:
                    tmp.kwargs.update({'gen_num':n, 'best_index':tmp.best_index,\
                                       'best_score':round(tmp.pool_score_best, 3),\
                                       'mean_score':round(tmp.pool_score_mean + tmp.aim, 3),\
                                       'time':round(time.time() - tmp.start, 3)})
                    tmp.show_pool_func(tmp.pool, **tmp.kwargs)
                    
            #end check
            if tmp.check_save_mean():
                count = 0
            else:
                count += 1
            if count >= tmp.para_num*5:
                break
        
        #==============================================================
        #show
        if tmp.show_pool_func != None:
            tmp.kwargs.update({'gen_num':n, 'best_index':tmp.best_index,\
                               'best_score':round(tmp.pool_score_best, 3),\
                               'mean_score':round(tmp.pool_score_mean + tmp.aim, 3),\
                               'time':round(time.time() - tmp.start, 3)})
            tmp.show_pool_func(tmp.pool, **tmp.kwargs)
        #2-opt
        tmp.pool_best, tmp.pool_score_best = self.opt2(tmp.pool_best, tmp.score_func, tmp.aim,\
                                                       show_para_func=show_para_func, **tmp.kwargs)
        #==============================================================
        return tmp.pool_best, tmp.pool_score_best
    
    
    
    
    #==============================================================#==============================================================
    #==============================================================#==============================================================
    def dcGA(self, para_range, score_func, aim, show_pool_func=None, show_para_func=None, seed=None, verbose=0, **kwargs):#, maxgen=5000):
        #
        tmp = setting(para_range, score_func, aim, show_pool_func, show_para_func, seed, verbose, **kwargs)
        if verbose >= 1:
            tmp.set_hyper(tmp.para_num*50, 2, 6)
        else:
            tmp.set_hyper(tmp.para_num*10, 2, 6)
        tmp.set_pool(int)
        
        #3 choices
        tmp.choice = np.array([[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0]], dtype=int)
        
        #gen 1 pool
        for i in range(tmp.pool_num):
            for j in range(tmp.para_num):
                tmp.pool[i, j] = nr.choice(tmp.para_range[j])
        
        #
        tmp.score_pool()
        tmp.save_best()
        tmp.save_mean()
        
        #show
        if tmp.show_pool_func != None:
            tmp.kwargs.update({'gen_num':0, 'best_index':tmp.best_index,\
                               'best_score':round(tmp.pool_score_best, 3),\
                               'mean_score':round(tmp.pool_score_mean + tmp.aim, 3),\
                               'time':round(time.time() - tmp.start, 3)})
            tmp.show_pool_func(tmp.pool, **tmp.kwargs)
        
        #gen 2-
        count = 0
        for n in range(1, 1000000 + 1):
            #
            tmp.make_parent()
            
            #2-point cross
            #==============================================================
            #cross point
            cross_point = nr.choice(range(1, tmp.para_num), 2, replace = False)
            if cross_point[0] > cross_point[1]:
                cross_point[0], cross_point[1] = cross_point[1], cross_point[0]
            #child
            for i in range(len(tmp.choice)):
                tmp.child[i] = np.hstack((tmp.parent[tmp.choice[i, 0], :cross_point[0]],
                                          tmp.parent[tmp.choice[i, 1], cross_point[0]:cross_point[1]],
                                          tmp.parent[tmp.choice[i, 2], cross_point[1]:]))
            #==============================================================
            #mutation
            #==============================================================
            for ch in tmp.child:
                for j in range(tmp.para_num):
                    if nr.rand() < (1.0 / tmp.para_num):
                        ch[j] = nr.choice(tmp.para_range[j])
            #==============================================================
            
            #
            tmp.score_child()
            tmp.make_family()
            tmp.JGG()
            tmp.check_save_best()
            
            #show
            if n % (tmp.pool_num//2) == 0 and tmp.show_pool_func != None:
                if tmp.show_pool_func != None:
                    tmp.kwargs.update({'gen_num':n, 'best_index':tmp.best_index,\
                                       'best_score':round(tmp.pool_score_best, 3),\
                                       'mean_score':round(tmp.pool_score_mean + tmp.aim, 3),\
                                       'time':round(time.time() - tmp.start, 3)})
                    tmp.show_pool_func(tmp.pool, **tmp.kwargs)
                    
            #end check
            if tmp.check_save_mean():
                count = 0
            else:
                count += 1
            if count >= tmp.para_num*5:
                break
        
        #==============================================================
        #show
        if tmp.show_pool_func != None:
            tmp.kwargs.update({'gen_num':n, 'best_index':tmp.best_index,\
                               'best_score':round(tmp.pool_score_best, 3),\
                               'mean_score':round(tmp.pool_score_mean + tmp.aim, 3),\
                               'time':round(time.time() - tmp.start, 3)})
            tmp.show_pool_func(tmp.pool, **tmp.kwargs)
        #2-opt
        tmp.pool_best, tmp.pool_score_best = self.opt2(tmp.pool_best, tmp.score_func, tmp.aim,\
                                                       show_para_func=show_para_func, **tmp.kwargs)
        #==============================================================
        return tmp.pool_best, tmp.pool_score_best
        
        
        
        
    #==============================================================#==============================================================
    #==============================================================#==============================================================
    def rcGA(self, para_range, score_func, aim, show_pool_func=None, show_para_func=None, seed=None, verbose=0, **kwargs):
        #
        tmp = setting(para_range, score_func, aim, show_pool_func, show_para_func, seed, verbose, **kwargs)
        if verbose >= 1:
            tmp.set_hyper(tmp.para_num*50, tmp.para_num*2, tmp.para_num*10)
        else:
            tmp.set_hyper(tmp.para_num*10, tmp.para_num*2, tmp.para_num*10)
        tmp.set_pool(float)
        
        #
        tmp.ave, tmp.sd = np.zeros(tmp.para_num), 1.0 / math.sqrt(tmp.parent_num)
        
        #gen 1 pool
        for j in range(tmp.para_num):
            tmp.pool[:, j] = nr.rand(tmp.pool_num) * (tmp.para_range[j, 1] - tmp.para_range[j, 0]) + tmp.para_range[j, 0]

        #
        tmp.score_pool()
        tmp.save_best()
        tmp.save_mean()
        
        #show
        if tmp.show_pool_func != None:
            tmp.kwargs.update({'gen_num':0, 'best_index':tmp.best_index,\
                               'best_score':round(tmp.pool_score_best, 3),\
                               'mean_score':round(tmp.pool_score_mean + tmp.aim, 3),\
                               'time':round(time.time() - tmp.start, 3)})
            tmp.show_pool_func(tmp.pool, **tmp.kwargs)
        
        #gen 2-
        count = 0
        for n in range(1, 1000000 + 1):
            #
            tmp.make_parent()
            
            #parant average
            tmp.ave = np.mean(tmp.parent, axis=0)
            
            #REX
            #==============================================================
            #child
            tmp.child[:, :] = float('inf')
            for i in range(tmp.child_num):
                for j in range(tmp.para_num):
                    while tmp.child[i, j] < tmp.para_range[j, 0] or tmp.para_range[j, 1] < tmp.child[i, j]:
                        #average
                        tmp.child[i, j] = tmp.ave[j]
                        #perturbation
                        for k in range(tmp.parent_num):
                            tmp.child[i, j] += nr.normal(0, tmp.sd) * (tmp.parent[k][j] - tmp.ave[j])
            #==============================================================
            
            tmp.score_child()
            tmp.make_family()
            tmp.JGG()
            tmp.check_save_best()
            
            #show
            if n % (tmp.pool_num//2) == 0 and tmp.show_pool_func != None:
                if tmp.show_pool_func != None:
                    tmp.kwargs.update({'gen_num':n, 'best_index':tmp.best_index,\
                                       'best_score':round(tmp.pool_score_best, 3),\
                                       'mean_score':round(tmp.pool_score_mean + tmp.aim, 3),\
                                       'time':round(time.time() - tmp.start, 3)})
                    tmp.show_pool_func(tmp.pool, **tmp.kwargs)
                    
            #end check
            if tmp.check_save_mean():
                count = 0
            else:
                count += 1
            if count >= tmp.para_num*5:
                break
            
        #==============================================================
        #show
        if tmp.show_pool_func != None:
            tmp.kwargs.update({'gen_num':n, 'best_index':tmp.best_index,\
                               'best_score':round(tmp.pool_score_best, 3),\
                               'mean_score':round(tmp.pool_score_mean + tmp.aim, 3),\
                               'time':round(time.time() - tmp.start, 3)})
            tmp.show_pool_func(tmp.pool, **tmp.kwargs)
        #==============================================================
        return tmp.pool_best, tmp.pool_score_best
        
        
        

    
    








if __name__ == '__main__':
    
    def knapsack_score(para, **kwargs):
        money = para[0]*10000 + para[1]*5000 + para[2]*1000 + para[3]*500\
              + para[4]*100 + para[5]*50 + para[6]*10 + para[7]*5 + para[8]*1
        num = np.sum(para)
        
        #if money >= 65168: #[6, 1, 0, 0, 1, 1, 1, 1, 3]
        rate = 0.01
        return (abs(65168 - para[0]*10000) + 1)*rate\
               * (abs(65168 - para[0]*10000 - para[1]*5000) + 1)*rate\
               * (abs(65168 - para[0]*10000 - para[1]*5000 - para[2]*1000) + 1)*rate\
               * (abs(65168 - para[0]*10000 - para[1]*5000 - para[2]*1000 - para[3]*500) + 1)*rate\
               * (abs(65168 - para[0]*10000 - para[1]*5000 - para[2]*1000 - para[3]*500 - para[4]*100) + 1)*rate\
               * (abs(65168 - para[0]*10000 - para[1]*5000 - para[2]*1000 - para[3]*500 - para[4]*100 - para[5]*50) + 1)*rate\
               * (abs(65168 - para[0]*10000 - para[1]*5000 - para[2]*1000 - para[3]*500 - para[4]*100 - para[5]*50 - para[6]*10) + 1)*rate\
               * (abs(65168 - para[0]*10000 - para[1]*5000 - para[2]*1000 - para[3]*500 - para[4]*100 - para[5]*50 - para[6]*10 - para[7]*5) + 1)*rate\
               * (abs(65168 - para[0]*10000 - para[1]*5000 - para[2]*1000 - para[3]*500 - para[4]*100 - para[5]*50 - para[6]*10 - para[7]*5 - para[8]*1) + 1)*rate
        
        #else:
        #    return 999999

    #poolの可視化（主にGAに渡す）
    def show_pool3(pool, **kwargs):
        #独自の変数を受け取ります
        pass
        #任意で次の変数が使用できます
        gen_num = kwargs['gen_num']
        best_index = kwargs['best_index']
        best_score = kwargs['best_score']
        mean_score = kwargs['mean_score']
        time = kwargs['time']
        
        #プロット
        plt.figure(figsize=(10, 10))
        #poolを100個まで薄い黒でプロット
        x = np.arange(len(pool[:100]))
        plt.bar(x, pool[:100, 0]*10000)
        plt.bar(x, pool[:100, 1]*5000, bottom=pool[:, 0]*10000)
        plt.bar(x, pool[:100, 2]*1000, bottom=pool[:, 0]*10000 + pool[:, 1]*5000)
        #plt.bar(x, pool[:100, 3]*500,  bottom=pool[:, 0]*10000 + pool[:, 1]*5000 + pool[:, 2]*1000)
        #plt.bar(x, pool[:100, 4]*100,  bottom=pool[:, 0]*10000 + pool[:, 1]*5000 + pool[:, 2]*1000 + pool[:, 3]*500)
        '''
        plt.bar(x, pool[:100, 5]*50,   bottom=pool[:, 0]*10000 + pool[:, 1]*5000 + pool[:, 2]*1000 + pool[:, 3]*500\
                                             +pool[:, 4]*100)
        plt.bar(x, pool[:100, 6]*10,   bottom=pool[:, 0]*10000 + pool[:, 1]*5000 + pool[:, 2]*1000 + pool[:, 3]*500\
                                             +pool[:, 4]*100   + pool[:, 5]*50)
        plt.bar(x, pool[:100, 7]*5,    bottom=pool[:, 0]*10000 + pool[:, 1]*5000 + pool[:, 2]*1000 + pool[:, 3]*500\
                                             +pool[:, 4]*100   + pool[:, 5]*50   + pool[:, 6]*10)
        plt.bar(x, pool[:100, 8]*1,    bottom=pool[:, 0]*10000 + pool[:, 1]*5000 + pool[:, 2]*1000 + pool[:, 3]*500\
                                             +pool[:, 4]*100   + pool[:, 5]*50   + pool[:, 6]*10   + pool[:, 7]*5)'''
        #エリートは赤でプロット
        #plt.plot(pool[best_index, 0], pool[best_index, 1], 'or')
        #タイトルをつけて表示
        plt.title('gen={}, best={} mean={} time={}'.format(gen_num, best_score, mean_score, time))
        plt.ylim([0, 80000])
        #plt.savefig('save/1_{}.png'.format(print_num))
        plt.show()
        print()

    
    def create_tsp(town_num):
        #create tsp
        town_x, town_y = [], []
        rate1 = 0.9
        rate2 = 0.3
        rate3 = 0.2
        for i in range(0, 360, 360//(town_num//4)):
            #print(i)
            town_x.append(math.sin(math.radians(i)))
            town_y.append(math.cos(math.radians(i)))
            town_x.append(rate1 * math.sin(math.radians(i)))
            town_y.append(rate1 * math.cos(math.radians(i)))
            town_x.append(rate2 * math.sin(math.radians(i)))
            town_y.append(rate2 * math.cos(math.radians(i)))
            town_x.append(rate3 * math.sin(math.radians(i)))
            town_y.append(rate3 * math.cos(math.radians(i)))
            #town_x.append(0.8**4 * math.sin(math.radians(i)))
            #town_y.append(0.8**4 * math.cos(math.radians(i)))
        town_x = np.array(town_x)
        town_y = np.array(town_y)
        
        town_x = nr.rand(town_num)
        town_y = nr.rand(town_num)
        
        return town_x, town_y
    
    
    def tsp_score(para, **kwargs):
        town_x = kwargs['town_x']
        town_y = kwargs['town_y']
        return np.sum(((town_x[para][:-1] - town_x[para][1:])**2 + (town_y[para][:-1] - town_y[para][1:])**2)**0.5)
    
    
    #paraの可視化（主に2-optに渡す）
    def show_para(para, **kwargs):
        #独自の変数を受け取ります
        town_x = kwargs['town_x']
        town_y = kwargs['town_y']
        #任意で次の変数が使用できます
        step_num = kwargs['step_num']
        score = kwargs['score']
        
        #プロット
        plt.figure(figsize=(10, 10))
        plt.plot(town_x[para], town_y[para], 'ok-')
        #タイトルをつけて表示
        plt.title('step={}, score={}'.format(step_num, score))
        #plt.savefig('save/1_{}.png'.format(print_num))
        plt.show()
        print()
    
    #poolの可視化（主にGAに渡す）
    def show_pool(pool, **kwargs):
        #独自の変数を受け取ります
        town_x = kwargs['town_x']
        town_y = kwargs['town_y']
        #任意で次の変数が使用できます
        gen_num = kwargs['gen_num']
        best_index = kwargs['best_index']
        best_score = kwargs['best_score']
        mean_score = kwargs['mean_score']
        time = kwargs['time']
        
        #プロット
        plt.figure(figsize=(10, 10))
        #poolを100個まで薄い黒でプロット
        for para in pool[:100]:
            plt.plot(town_x[para], town_y[para], 'ok-', alpha=(2.0/len(pool[:100])))
        #エリートは赤でプロット     
        plt.plot(town_x[pool[best_index]], town_y[pool[best_index]], 'or-')
        #タイトルをつけて表示
        plt.title('gen={}, best={} mean={} time={}'.format(gen_num, best_score, mean_score, time))
        #plt.savefig('save/1_{}.png'.format(print_num))
        plt.show()
        print()

    
    def rastrigin_score(para, **kwargs):
        k = 0
        for x in para:
            k += 10 + (x*x - 10 * math.cos(2*math.pi*x))
        return k
    
    
    #poolの可視化（主にGAに渡す）
    def show_pool2(pool, **kwargs):
        #独自の変数を受け取ります
        pass
        #任意で次の変数が使用できます
        gen_num = kwargs['gen_num']
        best_index = kwargs['best_index']
        best_score = kwargs['best_score']
        mean_score = kwargs['mean_score']
        time = kwargs['time']
        
        #プロット
        plt.figure(figsize=(10, 10))
        #poolを100個まで薄い黒でプロット
        plt.plot(pool[:100, 0], pool[:100, 1], 'ok', alpha=(10.0/len(pool[:100])))
        #エリートは赤でプロット
        plt.plot(pool[best_index, 0], pool[best_index, 1], 'or')
        #タイトルをつけて表示
        plt.title('gen={}, best={} mean={} time={}'.format(gen_num, best_score, mean_score, time))
        plt.xlim([-5, 5]); plt.ylim([-5, 5])
        #plt.savefig('save/1_{}.png'.format(print_num))
        plt.show()
        print()
    
    
    
    
    

    
    
    #do_tsp()
    
    
    
    #paraからスコアを返す関数
    #def func(para, **kwargs):
    
    #paraを可視化する関数
    #def func(para, **kwargs):
    
    #poolを可視化する関数
    #def func(pool, **kwargs):
    
    #2-opt法の使い方
    #opt2(para, score_func, show_func=None, **kwargs):
    
    
    
    
    
    
    #パラメータ範囲
    para_range = [[i for i in range(10)] for j in range(9)]
    #GA
    para, score = vcopt().dcGA(para_range,                #para
                               knapsack_score,            #score_func
                               0.0,                       #aim
                               show_pool_func=None, #show_para_func=None
                               show_para_func=None,       #show_para_func=None
                               seed=None,                 #seed=None
                               verbose=0)                 #verbose=0 (or 1,2,3)
    print(para, score)
    
    
    
    
    
    
    #巡回セールスマン問題の作成
    num = 15
    nr.seed(2)
    town_x, town_y = create_tsp(num)
    
    '''
    #パラメータの初期化
    para = np.arange(num)
    #2-opt
    para, score = vcopt().opt2(para,                     #para
                               tsp_score,                #score_func
                               0.0,                      #aim
                               show_para_func=show_para, #show_para_func=None
                               seed=None,                #seed=None
                               town_x=town_x,            #other your variables
                               town_y=town_y)
    '''
    
    '''
    #パラメータ範囲
    para_range = np.arange(num)
    #GA
    para, score = vcopt().tspGA(para_range,                #para
                                tsp_score,                 #score_func
                                0.0,                       #aim
                                show_pool_func=show_pool,  #show_para_func=None
                                show_para_func=show_para,  #show_para_func=None
                                seed=None,                 #seed=None
                                verbose=0,                 #verbose=0 (or 1,2,3)
                                town_x=town_x,             #other your variables
                                town_y=town_y)
    '''
    
    
    '''
    #パラメータ範囲
    para_range = [[-5, 5], [-5, 5], [-5, 5], [-5, 5], [-5, 5]]
    #GA
    para, score = vcopt().rcGA(para_range,                 #para
                                rastrigin_score,           #score_func
                                0.0,                       #aim
                                show_pool_func=show_pool2, #show_para_func=None
                                show_para_func=None,       #show_para_func=None
                                seed=None,                 #seed=None
                                verbose=0)                 #verbose=0 (or 1,2,3)
    '''
    
    
    
    
    
    
    
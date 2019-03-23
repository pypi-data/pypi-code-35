# -*- coding: utf-8 -*-
import numpy as np
import numpy.random as nr
import math, time
from copy import deepcopy
import matplotlib.pyplot as plt
np.set_printoptions(threshold=np.inf, precision=8, suppress=True, floatmode='maxprec')



class vcopt:
    def __init__(self):
        pass
    def __del__(self):
        pass
    
    #setting
    def setting(self, para_range, score_func, aim, show_pool_func, show_para_func, seed, verbose, **kwargs):
        self.para_range = np.array(para_range)
        self.para_num = len(para_range)
        self.score_func = score_func
        self.aim = aim
        self.show_para_func = show_para_func
        self.show_pool_func = show_pool_func
        self.seed = seed
        nr.seed(self.seed)
        self.verbose = verbose
        self.kwargs = kwargs
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
        #pool_score_best is the score
        self.pool_best = deepcopy(self.pool[self.best_index])
        self.pool_score_best = deepcopy(self.pool_score[self.best_index])

    #save mean
    def save_mean(self):
        #pool_score_mean is a pseudo score
        self.mean_abs_gap = np.mean(np.abs(self.aim - self.pool_score))
        if self.aim < self.pool_score_best:
            self.pool_score_mean = self.aim + self.mean_abs_gap
        else:
            self.pool_score_mean = self.aim - self.mean_abs_gap
        self.mean_abs_gap_save = deepcopy(self.mean_abs_gap)

    #make parent
    def make_parent(self, it):
        #self.pool_select = nr.choice(range(self.pool_num), self.parent_num, replace = False)
        self.pool_select = it
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
            self.save_best()
            return True
        else:
            return False

    #check and save mean
    def check_save_mean(self):
        self.mean_abs_gap = np.mean(np.abs(self.aim - self.pool_score))
        if self.mean_abs_gap < self.mean_abs_gap_save:
            #update
            self.save_mean()
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
        
    def show_pool(self, n):
        self.kwargs.update({'gen_num':n, 'best_index':self.best_index,\
                            'best_score':round(self.pool_score_best, 4),\
                            'mean_score':round(self.pool_score_mean, 4),\
                            'time':round(time.time() - self.start, 2)})
        self.show_pool_func(self.pool, **self.kwargs)
    
    #print bar final
    def print_bar_final(self, n):
        n0 = int(20*n/(self.maxgen+1)) + 1
        n1 = 20 - n0
        t = time.time() - self.start
        bar = '\r{}% [{}{}] time:{}s gen:{}  φ(□　□*)!!'.format(str((n*100//self.maxgen)).rjust(3), '#'*n0, ' '*n1, np.round(t, 1), n)
        #print(bar, end='')
        print(bar)
    
    #2-opt
    def opt2(self, para, score_func, aim, show_para_func=None, seed=None, step_max=float('inf'), **kwargs):
        #
        para, score = np.array(para), score_func(para, **kwargs)
        if seed != 'pass': nr.seed(seed)
        step = 0
        #
        if show_para_func != None:
            kwargs.update({'step_num':step, 'score':round(score, 3)})
            show_para_func(para, **kwargs)
        #opt
        while 1:
            update = False
            if step >= step_max:
                #print('stop')
                break
            
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
                #print('end')
                break
        return para, score





    #######################################################################################################################
    #######################################################################################################################
    def tspGA(self, para_range, score_func, aim, show_pool_func=None, show_para_func=None, seed=None, verbose=0, **kwargs):
        #
        self.setting(para_range, score_func, aim, show_pool_func, show_para_func, seed, verbose, **kwargs)
        #self.set_hyper(self.para_num*10, self.para_num*1, self.para_num*1)
        self.set_hyper(self.para_num*10, 2, 2)
        self.set_pool(int)
        
        self.opt2_num = 1
        
        #gen 1 pool
        for i in range(self.pool_num):
            self.pool[i] = deepcopy(self.para_range)
            nr.shuffle(self.pool[i])
            #mini 2-opt
            self.pool[i], self.pool_score[i] = self.opt2(self.pool[i], self.score_func, self.aim,\
                                                         seed='pass', step_max=self.opt2_num, **self.kwargs)
        
        #
        #self.score_pool()
        self.save_best()
        self.save_mean()
        
        #show
        if self.show_pool_func != None:
            self.show_pool(0)
        
        #gen 2-
        #count = 0
        for n in range(1, 1000000 + 1):
            #
            #self.make_parent()
            
            self.opt2_num = n // 10
            #print(self.opt2_num)
            
            #iteration
            iteration = np.arange(self.pool_num)
            nr.shuffle(iteration)
            iteration = iteration.reshape((self.pool_num//self.parent_num), self.parent_num)
            for it in iteration:
                #
                self.make_parent(it)            
            
                #辺に着目したヒュリスティック操作
                #==============================================================
                #ex_parent
                #self.ex_parent = np.hstack((self.parent[:, -1].reshape(self.parent_num, 1), self.parent, self.parent[:, 0].reshape(self.parent_num, 1)))
                self.ex_parent = np.hstack((self.parent[:, -3:].reshape(self.parent_num, 3), self.parent, self.parent[:, :3].reshape(self.parent_num, 3)))
                #print(self.parent)
                #print(self.ex_parent)
                #child
                for i in range(self.child_num):
                    #first para
                    s = self.parent[nr.randint(self.parent_num), 0]
                    if nr.rand() < (1.0 / self.para_num):
                        s = self.para_range[nr.randint(self.para_num)]
                    #s = self.para_range[nr.randint(self.para_num)]
                    self.child[i, 0] = s
                    #following para
                    for j in range(1, self.para_num):
                        
                        #left right mask of ex_parent
                        #mask = np.zeros((self.parent_num, self.para_num + 2), dtype=bool)
                        #true left
                        #mask[:, :-2] += (self.parent == s)
                        #true right
                        #mask[:, 2:] += (self.parent == s)
                        #print(self.child)
                        
                        mask_3 = np.zeros((self.parent_num, self.para_num + 6), dtype=bool)
                        mask_2 = np.zeros((self.parent_num, self.para_num + 6), dtype=bool)
                        #mask_1 = np.zeros((self.parent_num, self.para_num + 6), dtype=bool)
                        mask_3[:, 4:-2] += (self.parent == s)
                        mask_3[:, 2:-4] += (self.parent == s)
                        mask_2[:, 5:-1] += (self.parent == s)
                        mask_2[:, 1:-5] += (self.parent == s)
                        #mask_1[:, 6:] += (self.parent == s)
                        #mask_1[:, :-6] += (self.parent == s)
                        #print(mask_1)
                        
                        #p (index in para_range)
                        p = np.ones(self.para_num) * (1.0 / self.para_num)
                        for k in self.ex_parent[mask_3]:
                            p[np.where(self.para_range==k)[0]] += 1.0 / self.parent_num
                        for k in self.ex_parent[mask_2]:
                            p[np.where(self.para_range==k)[0]] += 0.1 / self.parent_num
                        #for k in self.ex_parent[mask_1]:
                        #    p[np.where(self.para_range==k)[0]] += 0.1
                        
                        #print(p)
                        #mask passed para
                        for k in self.child[i, 0:j]:
                            p[np.where(self.para_range==k)[0]] = 0.0
                        
                        #choice
                        p *= 1.0 / np.sum(p)
                        s = nr.choice(self.para_range, p=p)
                        #child
                        self.child[i, j] = s
                #==============================================================
                #
                #self.score_child()
                self.make_family()
                #mini 2-opt
                for i in range(self.parent_num + self.child_num):
                    self.family[i], self.family_score[i] = self.opt2(self.family[i], self.score_func, self.aim,\
                                                                     seed='pass', step_max=self.opt2_num, **self.kwargs)
                self.JGG()
            
            self.check_save_best()
            
            #show
            if self.show_pool_func != None:
                self.show_pool(n * self.pool_num)
            
            #end check
            if self.check_save_mean():
                pass
            else:
                break
        
        #show
        #if self.show_pool_func != None:
        #    self.show_pool(n * self.pool_num)
        #2-opt
        #self.pool_best, self.pool_score_best = self.opt2(self.pool_best, self.score_func, self.aim,\
        #                                                 seed='pass', show_para_func=self.show_para_func, **self.kwargs)
        return self.pool_best, self.pool_score_best
    
    
    
    
    #==============================================================#==============================================================
    #==============================================================#==============================================================
    def dcGA(self, para_range, score_func, aim, show_pool_func=None, show_para_func=None, seed=None, verbose=0, **kwargs):
        #
        self.setting(para_range, score_func, aim, show_pool_func, show_para_func, seed, verbose, **kwargs)
        self.set_hyper(self.para_num*10, 2, 6)
        self.set_pool(int)
        
        #3 choices
        self.choice = np.array([[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0]], dtype=int)
        
        #gen 1 pool
        for i in range(self.pool_num):
            for j in range(self.para_num):
                self.pool[i, j] = nr.choice(self.para_range[j])
        
        #
        self.score_pool()
        self.save_best()
        self.save_mean()
        
        #show
        if self.show_pool_func != None:
            self.show_pool(0)
        
        #gen 2-
        #count = 0
        for n in range(1, 1000000 + 1):
            #
            #self.make_parent()
            #iteration
            iteration = np.arange(self.pool_num)
            nr.shuffle(iteration)
            iteration = iteration.reshape((self.pool_num//self.parent_num), self.parent_num)
            for it in iteration:
                #
                self.make_parent(it)            
            
                #2-point cross
                #==============================================================
                #cross point
                cross_point = nr.choice(range(1, self.para_num), 2, replace = False)
                if cross_point[0] > cross_point[1]:
                    cross_point[0], cross_point[1] = cross_point[1], cross_point[0]
                #child
                for i in range(len(self.choice)):
                    self.child[i] = np.hstack((self.parent[self.choice[i, 0], :cross_point[0]],
                                               self.parent[self.choice[i, 1], cross_point[0]:cross_point[1]],
                                               self.parent[self.choice[i, 2], cross_point[1]:]))
                #==============================================================
                #mutation
                #==============================================================
                for ch in self.child:
                    for j in range(self.para_num):
                        if nr.rand() < (1.0 / self.para_num):
                            ch[j] = nr.choice(self.para_range[j])
                #==============================================================
                #
                self.score_child()
                self.make_family()
                self.JGG()
            
            self.check_save_best()
            
            #show
            if self.show_pool_func != None:
                self.show_pool(n * self.pool_num)
                    
            #end check
            if self.check_save_mean():
                pass
            else:
                break

        return self.pool_best, self.pool_score_best
        
        
        
        
    #==============================================================#==============================================================
    #==============================================================#==============================================================
    def rcGA(self, para_range, score_func, aim, show_pool_func=None, show_para_func=None, seed=None, verbose=0, **kwargs):
        #
        self.setting(para_range, score_func, aim, show_pool_func, show_para_func, seed, verbose, **kwargs)
        self.set_hyper(self.para_num*10, self.para_num*1, self.para_num*10)
        if self.para_num >= 10: self.set_hyper(self.para_num*12, self.para_num*1, self.para_num*12)
        if self.para_num >= 20: self.set_hyper(self.para_num*15, self.para_num*1, self.para_num*15)
        if self.para_num >= 50: self.set_hyper(self.para_num*20, self.para_num*1, self.para_num*20)
        
        self.set_pool(float)
        
        #
        self.sd = 1.0*0.9 / math.sqrt(self.parent_num)
        
        #gen 1 pool
        for j in range(self.para_num):
            self.pool[:, j] = nr.rand(self.pool_num) * (self.para_range[j, 1] - self.para_range[j, 0]) + self.para_range[j, 0]
        
        #
        self.score_pool()
        self.save_best()
        self.save_mean()
        
        #show
        if self.show_pool_func != None:
            self.show_pool(0)
        
        #gen 2-
        #count = 0
        for n in range(1, 1000000 + 1):
            #
            #self.make_parent()
            #iteration
            iteration = np.arange(self.pool_num)
            nr.shuffle(iteration)
            iteration = iteration.reshape((self.pool_num//self.parent_num), self.parent_num)
            for it in iteration:
                #
                self.make_parent(it)            

                #REX
                #==============================================================
                #parant average
                ave = np.mean(self.parent, axis=0)
                #child
                self.child[:, :] = float('inf')
                for i in range(self.child_num):
                    for j in range(self.para_num):
                        while self.child[i, j] < self.para_range[j, 0] or self.para_range[j, 1] < self.child[i, j]:
                            #average
                            self.child[i, j] = ave[j]
                            #perturbation
                            for k in range(self.parent_num):
                                self.child[i, j] += nr.normal(0, self.sd) * (self.parent[k][j] - ave[j])
                #==============================================================
                #
                self.score_child()
                self.make_family()
                self.JGG()
            self.check_save_best()
            
            #show
            if self.show_pool_func != None:
                self.show_pool(n * self.pool_num)
            
            #end check
            if self.check_save_mean() and np.max(np.std(self.pool, axis=0) / [self.para_range[:, 1] - self.para_range[:, 0]]) > 0.0001:
                pass
            else:
                break

        return self.pool_best, self.pool_score_best
    
    
    
    
    


    
























if __name__ == '__main__':

    
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
        
        para_full = np.hstack((0, para, 0))
        #print(para_full)
        
        return np.sum(((town_x[para_full][:-1] - town_x[para_full][1:])**2 + (town_y[para_full][:-1] - town_y[para_full][1:])**2)**0.5)
    
    
    #paraの可視化（主に2-optに渡す）
    def show_para(para, **kwargs):
        #独自の変数を受け取ります
        town_x = kwargs['town_x']
        town_y = kwargs['town_y']
        #任意で次の変数が使用できます
        step_num = kwargs['step_num']
        score = kwargs['score']
        
        para_full = np.hstack((0, para, 0))
        #print(para_full)
        
        #プロット
        plt.figure(figsize=(6, 6))
        plt.plot(town_x[para_full], town_y[para_full], 'ok-')
        plt.plot(town_x[0], town_y[0], 'or-')
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
        
        pool_full = np.hstack((np.zeros(len(pool), dtype=int).reshape(len(pool), 1), pool, (np.zeros(len(pool), dtype=int).reshape(len(pool), 1))))
        
        #プロット
        plt.figure(figsize=(6, 6))
        #poolを100個まで薄い黒でプロット
        for para in pool_full[:100]:
            plt.plot(town_x[para], town_y[para], 'ok-', alpha=(2.0/len(pool[:100])))
        #エリートは赤でプロット     
        plt.plot(town_x[pool_full[best_index]], town_y[pool_full[best_index]], 'or-')
        #タイトルをつけて表示
        plt.title('gen={}, best={} mean={} time={}'.format(gen_num, best_score, mean_score, time))
        #plt.savefig('save/1_{}.png'.format(print_num))
        plt.show()
        print()

    
    #ナップザック問題の評価関数
    def money_score(para, **kwargs):
        
        money = para[0]*10000 + para[1]*5000 + para[2]*1000 + para[3]*500 + para[4]*100 + para[5]*50 + para[6]*10
        num = np.sum(para)
        
        #スコアの計算（直接returnする）
        return (abs(65860 - money) + 1) * num**2

    #poolの可視化
    def money_show_pool(pool, **kwargs):
        
        #任意で次の変数が使用できます
        gen_num = kwargs['gen_num']
        best_index = kwargs['best_index']
        best_score = kwargs['best_score']
        mean_score = kwargs['mean_score']
        time = kwargs['time']
        
        #プロット（および保存）
        plt.figure(figsize=(6, 6))
        #poolを100個まで積み上げ棒グラフでプロット
        x = np.arange(len(pool[:100]))
        plt.bar(x, pool[:100, 0]*10000)
        plt.bar(x, pool[:100, 1]*5000, bottom=pool[:, 0]*10000)
        plt.bar(x, pool[:100, 2]*1000, bottom=pool[:, 0]*10000 + pool[:, 1]*5000)
        plt.bar(x, pool[:100, 3]*500,  bottom=pool[:, 0]*10000 + pool[:, 1]*5000 + pool[:, 2]*1000)
        plt.bar(x, pool[:100, 4]*100,  bottom=pool[:, 0]*10000 + pool[:, 1]*5000 + pool[:, 2]*1000 + pool[:, 3]*500)
        plt.bar(x, pool[:100, 5]*50,   bottom=pool[:, 0]*10000 + pool[:, 1]*5000 + pool[:, 2]*1000 + pool[:, 3]*500 + pool[:, 4]*100)
        plt.bar(x, pool[:100, 6]*10,   bottom=pool[:, 0]*10000 + pool[:, 1]*5000 + pool[:, 2]*1000 + pool[:, 3]*500 + pool[:, 4]*100 + pool[:, 5]*50)
        #タイトルをつけて表示
        plt.title('gen={}, best={} mean={} time={}'.format(gen_num, best_score, mean_score, time))
        plt.ylim([0, 80000])
        #plt.savefig('save/GA_{}.png'.format(gen_num))
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
        plt.figure(figsize=(6, 6))
        
        #次元の数だけ横選
        for dim in range(len(pool[0])):
            plt.plot([-5, 5], [dim, dim], 'k-')
        #poolを次元ごとに100個まで薄い黒でプロット
        for dim in range(len(pool[0])):
            plt.plot(pool[:100, dim], [dim]*len(pool[:100]), 'ok', markersize=8, alpha=(2.0/len(pool[:100])))
        #エリートは赤でプロット
        plt.plot(pool[best_index, :], range(len(pool[0])), 'or', markersize=8)
        #タイトルをつけて表示
        plt.title('gen={}, best={} mean={} time={}'.format(gen_num, best_score, mean_score, time))
        #plt.savefig('save/1_{}.png'.format(print_num))
        plt.show()
        print()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
  
    
    #巡回セールスマン問題の作成
    num = 20
    nr.seed(1)
    town_x, town_y = create_tsp(num)
    
    '''
    #パラメータの初期化
    para = np.arange(1, num)
    #2-opt
    para, score = vcopt().opt2(para,                     #para
                               tsp_score,                #score_func
                               0.0,                      #aim
                               show_para_func=show_para, #show_para_func=None
                               seed=None,                #seed=None
                               town_x=town_x,            #other your variables
                               town_y=town_y)
    '''
    
    
    #パラメータ範囲
    para_range = np.arange(1, num)
    #GA
    para, score = vcopt().tspGA(para_range,                #para
                                tsp_score,                 #score_func
                                0.0,                       #aim
                                show_pool_func=show_pool,  #show_para_func=None
                                show_para_func=show_para,  #show_para_func=None
                                seed=1,                 #seed=None
                                verbose=0,                 #verbose=0 (or 1,2,3)
                                town_x=town_x,             #other your variables
                                town_y=town_y)
    
    
 
    
    
    
    
    
    
    
    
    
    
    
    '''
    #パラメータ範囲
    para_range = [[i for i in range(10)] for j in range(7)]
    
    #GAで最適化
    para, score = vcopt().dcGA(para_range,                      #para_range
                               money_score,                     #score_func
                               0.0,                             #aim
                               show_pool_func=money_show_pool,  #show_para_func=None
                               show_para_func=None,             #show_para_func=None
                               seed=0,                       #seed=None
                               verbose=0)                       #verbose=0 (or 1,2,3)
    
    #結果の表示
    print(para)
    print(score)
    '''
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    '''
    #パラメータ範囲
    para_range = np.ones((15, 2)) * 5
    para_range[:, 0] *= -1
    
    #GA
    para, score = vcopt().rcGA(para_range,                 #para
                                rastrigin_score,           #score_func
                                -999,                       #aim
                                show_pool_func=show_pool2, #show_para_func=None
                                show_para_func=None,       #show_para_func=None
                                seed=None,                 #seed=None
                                verbose=0)                 #verbose=0 (or 1,2,3)
    '''
    
    
    
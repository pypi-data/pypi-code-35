# -*- coding: utf-8 -*-
import os
import time
import numpy as np
import warnings
import matplotlib.cbook
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
from sklearn import manifold
from sklearn.preprocessing import MinMaxScaler

class Result(object):
    def dict2array(self, table_head, recording_dict):
        recording = list()
        for key in table_head:
            recording.append(np.array(recording_dict[key],dtype= np.float32).reshape(-1,1))
        recording = np.concatenate(recording,axis = 1)
        # recording = np.concatenate((table_head.reshape(1,-1),recording),axis = 0)
        return recording
    
    def save_result_to_csv(self):
        print("Save result...")
        path = '../result/' + self.save_name + '/'
        if not os.path.exists(path): os.makedirs(path)
        if self.task == 'classification':
            epoch_table_head = ['epoch','time','loss','train_accuracy','test_accuracy']
            best_table_head = ['FDR','FPR']
            # pred_cnt
            self.label_cnt = np.array(self.best_dict['pred_cnt'],dtype = np.float32)
            np.savetxt(path + 'label_cnt['+self.name+'].csv', self.label_cnt, fmt='%.4f',delimiter=",")
            
        else:
            epoch_table_head = ['epoch','time','loss','train_rmse','train_R2','test_rmse','test_R2']
            best_table_head = ['rmse','R2']
        
        # epoch_recording
        self.epoch_result = self.dict2array(epoch_table_head, self.recording_dict)
        np.savetxt(path + 'epoch['+self.name+'].csv', self.epoch_result, fmt='%.4f',delimiter=",")
        
        # best_recording
        best_recording = self.dict2array(best_table_head, self.best_dict)
        if self.task == 'classification':
            average = np.array([self.best_dict['accuracy'],1-self.best_dict['accuracy']]).reshape(1,-1)
            best_recording = np.concatenate((best_recording,average),axis = 0)
        np.savetxt(path + 'best['+self.name+'].csv', best_recording, fmt='%.4f',delimiter=",")
        
        # pred
        # pred_head = ['real_Y','pred_Y']
        self.pred_result = np.array(self.pred_Y,dtype = np.float32).reshape(1,-1)
        if self.real_Y is not None:
            real_result = np.array(self.real_Y,dtype = np.float32).reshape(1,-1)
            self.pred_result = np.concatenate((real_result,self.pred_result))
        np.savetxt(path + 'pred['+self.name+'].csv', best_recording, fmt='%.4f',delimiter=",")
    
    def plot_curve(self, path, main_dict, twin_dict = None, show_result = True):
        '''
            dict = {'y': [data1,data2],
                    'legend': [str1,str2],
                    'y_label': str}
        '''
        
        plt.style.use('classic')
        fig = plt.figure(figsize=[32,18])
        
        y = main_dict['y']
        n = y.shape[0]
        x = range(1,n+1)
        
        ax1 = fig.add_subplot(111)
        if type(y) == list:
            ax1.plot(x, y[0],color='b',marker='o',markersize=10,linestyle='-.',linewidth=4,label='$'+main_dict['legend'][0]+'$')
            ax1.plot(x, y[1],color='g',marker='o',markersize=10,linestyle='-.',linewidth=4,label='$'+main_dict['legend'][1]+'$')
        else:
            ax1.plot(x, y,color='r',marker='o',markersize=10,linestyle='-.',linewidth=4,label='$'+main_dict['legend']+'$')
        ax1.set_ylabel('$'+ main_dict['y_label'] +'$',fontsize=36)
        #if self.title:
        #    ax1.set_title("Training loss and test accuracy")
        ax1.set_xlabel('$Epochs$',fontsize=36)
        legend = ax1.legend(loc='upper left',fontsize=24)
        legend.get_frame().set_facecolor('none')
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        
        if twin_dict is not None:
            y = twin_dict['y']
            
            ax2 = ax1.twinx()  # this is the important function
            if type(y) == list:
                ax2.plot(x, y[0],color='c',marker='D',markersize=10,linestyle='-',linewidth=4,label='$'+twin_dict['legend'][0]+'$')
                ax2.plot(x, y[1],color='m',marker='D',markersize=10,linestyle='-',linewidth=4,label='$'+twin_dict['legend'][1]+'$')
            else:
                ax2.plot(x, y,color='c',marker='D',markersize=10,linestyle='-',linewidth=4,label='$'+twin_dict['legend']+'$')
            ax2.set_ylabel('$'+twin_dict['y_label']+'$',fontsize=36)
            legend = ax2.legend(loc='upper right',fontsize=24)
            legend.get_frame().set_facecolor('none')
            plt.yticks(fontsize=20)
            
        plt.savefig(path +'.png', bbox_inches='tight')
        if show_result: plt.show()
        plt.close(fig)
    
    def plot_epoch_result(self):
        path = '../result/' + self.save_name + '/'
        if not os.path.exists(path): os.makedirs(path)
        
        if self.task == 'classification':
            print("Plot loss and accuracy curve...")
            main_dict = {'y': self.epoch_result[:,2],
                         'legend': 'Loss',
                         'y_label': 'Loss'}
            twin_dict = {'y': [self.epoch_result[:,3]*100,self.epoch_result[:,4]*100],
                         'legend': ['train\;accuracy','test\;accuracy'],
                         'y_label': 'Everage\;\;FDR\;(\%)'}
            path += 'epoch_accuracy['+self.name+']'
        else:
            print("Plot rmse curve...")
            main_dict = {'y': [self.epoch_result[:,3],self.epoch_result[:,5]],
                         'legend': ['train\;rmse','test\;rmse'],
                         'y_label': 'RMSE'}
            twin_dict = {'y': [self.epoch_result[:,4],self.epoch_result[:,6]],
                         'legend': ['train\;R2','test\;R2'],
                         'y_label': 'R2'}
            path += 'epoch_rmse['+self.name+']'
        self.plot_curve(path, main_dict, twin_dict = twin_dict, show_result =  self.show_result_in_console)
        
    def plot_pred_result(self, xticks = None, yticks = None):
        '''
            classification: sort = True -> 按标签将数据集排序
        '''
        path = '../result/' + self.save_name + '/'
        if not os.path.exists(path): os.makedirs(path)
        
        warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)
        print("Plot pred result...")
        
        plt.style.use('ggplot')
        n_sample = self.pred_Y.shape[0] # 预测样本总数
        x = np.asarray(range(1,n_sample+1))
        c = np.asarray(range(self.n_category))
        
        fig = plt.figure(figsize=[32,18])
        ax1 = fig.add_subplot(111)
        
        real_Y = self.real_Y; pred_Y = self.pred_Y
        if self.task == 'classification' and self.sort_pred_category:                              
            tup_list=list(zip(real_Y, pred_Y))
            tup_list.sort(key=lambda dic_zip: dic_zip[0])
            real_Y, pred_Y=map(list,zip(*tup_list))
            
        ax1.scatter(x, real_Y,alpha=0.75,color='none', edgecolor='red', s=20,label='$test\;category$')
        ax1.scatter(x, pred_Y,alpha=0.75,color='none', edgecolor='blue', s=20,label='$pred\;category$')
        #if self.title:
        #    ax1.set_title("Label Distribution",fontsize=36)
        ax1.set_xlabel('$Sample$',fontsize=36)
        if self.task == 'classification':
            ax1.set_ylabel('$Category$',fontsize=36)
        else:
            ax1.set_ylabel('$Prediction$',fontsize=36)
        ax1.legend(loc='upper left',fontsize=24)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        
        if xticks is not None: plt.xticks(xticks,fontsize=20)
        else: plt.xticks(fontsize=20)
        if yticks is not None: plt.yticks(c, yticks, rotation=0, fontsize=20)
        else: plt.yticks(fontsize=20)
        
        path += 'pred_result['+self.name+']'
        plt.savefig(path +'.png',bbox_inches='tight')
        if self.show_result_in_console: plt.show()
        plt.close(fig)
    
    def plot_label_cnt(self, path = None, name = None, category_ticks = None):
        if path is None: path = '../result/' + self.save_name + '/'
        if name is None: name = self.name
        if not os.path.exists(path): os.makedirs(path)
        
        plt.style.use('default')
        
        real_ticks = list()
        pred_ticks = list()
        if category_ticks is not None:
            for category in category_ticks:
                real_ticks.append('$'+category+'_r$')
                pred_ticks.append('$'+category+'_p$')
        else:
            for i in range(self.n_category):
                if i< 9: index = '0'+str(i+1)
                else: index = str(i+1)
                real_ticks.append('$Category'+ index +'_r$')
                pred_ticks.append('$Category'+ index +'_p$')
        real_ticks = np.concatenate(real_ticks)
        pred_ticks = np.concatenate(pred_ticks)
        
        size = 16
        ticksize = size/24*26
        fontsize = size/24*23
        
        fig =  plt.figure(figsize=[size,size])
        ax = fig.add_subplot(111)
        
        cmap = "gist_yarg"
        ax.imshow(self.label_cnt, cmap=cmap)
        
        #im = ax.imshow(self.label_cnt, cmap=cmap)
        #ax.figure.colorbar(im, ax=ax)
        
        plt.xticks(fontsize=ticksize)
        plt.yticks(fontsize=ticksize)
        
        ax.set_xticks(np.arange(len(real_ticks)))
        ax.set_yticks(np.arange(len(pred_ticks)))
    
        ax.set_xticklabels(real_ticks)
        ax.set_yticklabels(pred_ticks)
        
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                 rotation_mode="anchor") # 旋转
        
        for i in range(len(pred_ticks)):
            for j in range(len(real_ticks)):
                x = self.label_cnt[i,j]
                if x == 0 : cl = 'black'
                elif i!=j: cl = 'red'
                else:  cl = 'w'
                ax.text(j, i, x, ha="center", va="center", color=cl, fontsize=fontsize)
        
        path += 'label_cnt['+name+']'
        plt.savefig(path +'.png',bbox_inches='tight')
        plt.close(fig)
        
    def plot_tSNE(self,path = None, name = None, feature = None, label = None, filename = None):
        if path is None: path = '../result/' + self.save_name + '/'
        if name is None: name = self.name
        if not os.path.exists(path): os.makedirs(path)
        
        plt.style.use('default')
        print('Start t-SNE...')
        feature = MinMaxScaler().fit_transform(feature)
        if len(label.shape)>1 and label.shape[1]>1:
            label = np.array(np.argmax(label,axis=1).reshape(-1, 1),dtype=np.float32)
        color = MinMaxScaler().fit_transform(label).reshape(-1,)
        t0 = time()
        Y = manifold.TSNE(n_components=2, init='pca', random_state=0).fit_transform(feature)
    
        t1 = time()
        print("t-SNE: %.2g sec" % (t1 - t0))
        
        fig = plt.figure(figsize=[32,18])
        ax = fig.add_subplot(111)
        plt.scatter(Y[:, 0], Y[:, 1], c=color, cmap=plt.cm.Spectral)
        if filename is None: filename = 'tSNE_2d' 
        ax.xaxis.set_major_formatter(NullFormatter())
        ax.yaxis.set_major_formatter(NullFormatter())
        plt.axis('tight')
        
        path += 'tSNE['+name+']'
        plt.savefig(path +'.png',bbox_inches='tight')
        plt.close(fig)
    
"""
    cmap:
        Accent, Accent_r, Blues, Blues_r, BrBG, BrBG_r, BuGn, BuGn_r, BuPu, BuPu_r, CMRmap, CMRmap_r, 
        Dark2, Dark2_r, GnBu, GnBu_r, Greens, Greens_r, Greys, Greys_r, OrRd, OrRd_r, Oranges, Oranges_r, 
        PRGn, PRGn_r, Paired, Paired_r, Pastel1, Pastel1_r, Pastel2, Pastel2_r, PiYG, PiYG_r, 
        PuBu, PuBuGn, PuBuGn_r, PuBu_r, PuOr, PuOr_r, PuRd, PuRd_r, Purples, Purples_r, 
        RdBu, RdBu_r, RdGy, RdGy_r, RdPu, RdPu_r, RdYlBu, RdYlBu_r, RdYlGn, RdYlGn_r, Reds, Reds_r, 
        Set1, Set1_r, Set2, Set2_r, Set3, Set3_r, Spectral, Spectral_r, 
        Vega10, Vega10_r, Vega20, Vega20_r, Vega20b, Vega20b_r, Vega20c, Vega20c_r, 
        Wistia, Wistia_r, YlGn, YlGnBu, YlGnBu_r, YlGn_r, YlOrBr, YlOrBr_r, YlOrRd, YlOrRd_r, 
        afmhot, afmhot_r, autumn, autumn_r, binary, binary_r, bone, bone_r, brg, brg_r, bwr, bwr_r, 
        cool, cool_r, coolwarm, coolwarm_r, copper, copper_r, cubehelix, cubehelix_r, flag, flag_r, 
        gist_earth, gist_earth_r, gist_gray, gist_gray_r, gist_heat, gist_heat_r, gist_ncar, gist_ncar_r, 
        gist_rainbow, gist_rainbow_r, gist_stern, gist_stern_r, gist_yarg, gist_yarg_r, gnuplot, gnuplot2, 
        gnuplot2_r, gnuplot_r, gray, gray_r, hot, hot_r, hsv, hsv_r, inferno, inferno_r, jet, jet_r, 
        magma, magma_r, nipy_spectral, nipy_spectral_r, ocean, ocean_r, pink, pink_r, plasma, plasma_r, prism, prism_r, 
        rainbow, rainbow_r, seismic, seismic_r, spectral, spectral_r, spring, spring_r, summer, summer_r, 
        tab10, tab10_r, tab20, tab20_r, tab20b, tab20b_r, tab20c, tab20c_r, terrain, terrain_r, viridis, viridis_r, 
        winter, winter_r
"""
# -*- coding: utf-8 -*-


user_dict = {# load parameters
             'save_model': False,
             'load_phase':'',
             # tensorboard
             'open_tensorboard': False,
             # test after training
             'do_test': True,
             # save result to csv
             'save_result': True,
             # plot
             'plot_result': True,
             'show_result_in_console': True,
             'sort_pred_category': True
             }

hypp_dict = {# struct
             'struct': None,
             'hidden_func': ['gaussian','linear','linear'],
             'output_func': 'gaussian',
             'loss_func': 'mse',
             # train
             'opt': 'rmsp',
             'dropout_rate': 0.0,
             'decay_drop_rate': 1.0, # 0.382 * 0.995 ^ 240 = 0.1147
             'lr': 1e-3,
             'epoch': 180,
             'batch_size': 32
             }

SHOW_DICT = dict(hypp_dict)

base_dict = {# model
             'name': 'Model',
             'layer_list':list(),
             'is_sub': False,
             'hidden_activation_loc': 0,
             # train,test
             'input': None,
             'label': None,
             'output': None,
             'pred': None,
             'loss': None,
             'accuracy': None,
             'rmse':None,
             'R2':None,
             'batch_training': None,
             'merge':None,
             'save_name':None
             }

init_dict = {'sess': None,
             'saver': None,
             'tbd': None
             }

DATA_DICT = {'task': 'classification',
             'n_category': None,
             # setting
             'data_path': None,
             'split_rate': 0.0,
             'shuffle': False,
             'prep_x': '',
             'prep_y': False,
             'scaler_y': None,
             # datasets
             'datasets': None,
             'train_X': None,
             'train_Y': None,
             'test_X': None,
             'test_Y': None}

PASS_DICT = dict(DATA_DICT, **init_dict)
MODEL_DICT = dict(user_dict, **hypp_dict, **base_dict, **PASS_DICT)

pre_dict = {# hyperparameter
            'pre_lr': 1e-3,
            'pre_epoch': 35,      
            # base
            'name': 'Model',
            'struct': None,
            'recon': None,
            'is_sub': False, # 是否是子模型（RBM,AE）
            'is_pre': True,  # 是否进行预训练
            'sub_type':'rbm'
            }

rbm_dict = {# hyperparameter
            'unit_type':['gaussian','gaussian'],
            'cd_k':1,
            }
_ae_dict = {# hyperparameter
            'sub_func':['gaussian','linear'],
            'beta':0.5,        
            'prob':0.5,
            'noise_type':'gs',
            }

RBM_DICT = dict(pre_dict, **rbm_dict)
_AE_DICT = dict(pre_dict, **_ae_dict)
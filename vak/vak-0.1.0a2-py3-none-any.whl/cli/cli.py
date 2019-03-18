from .train import train
from .predict import predict
from .learncurve import learncurve
from .summary import summary
from .make_data import make_data
from ..config import parse


def cli(command, config_files):
    """command-line interface

    Parameters
    ----------
    command : string
        One of {'prep', 'train', 'predict', 'finetune', 'learncurve', 'summary'}
    config_files : string or list
        config.ini files
    """
    for config_file in config_files:
        config = parse.parse_config(config_file)

        if command == 'prep':
            raise NotImplementedError

        elif command == 'train':
            train(args.predict)

        elif command == 'finetune':
            raise NotImplementedError

        elif command == 'predict':
            predict(args.predict)

        elif command == 'learncurve':
                make_data(labelset=config.data.labelset,
                          all_labels_are_int=config.data.all_labels_are_int,
                          data_dir=config.data.data_dir,
                          total_train_set_dur=config.data.total_train_set_dur,
                          val_dur=config.data.val_dur,
                          test_dur=config.data.test_dur,
                          config_file=config_file,
                          silent_gap_label=config.data.silent_gap_label,
                          skip_files_with_labels_not_in_labelset=config.data.skip_files_with_labels_not_in_labelset,
                          output_dir=config.data.output_dir,
                          mat_spect_files_path=config.data.mat_spect_files_path,
                          mat_spects_annotation_file=config.data.mat_spects_annotation_file,
                          spect_params=config.spect_params)

                # get config again
                # because make_data changed train_data_dict_path and val_data_dict_path
                config = parse.parse_config(config_file)
                learncurve(train_data_dict_path=config.train.train_data_dict_path,
                           val_data_dict_path=config.train.val_data_dict_path,
                           spect_params=config.spect_params,
                           total_train_set_duration=config.data.total_train_set_dur,
                           train_set_durs=config.train.train_set_durs,
                           num_replicates=config.train.num_replicates,
                           num_epochs=config.train.num_epochs,
                           config_file=config_file,
                           networks=config.networks,
                           val_error_step=config.train.val_error_step,
                           checkpoint_step=config.train.checkpoint_step,
                           patience=config.train.patience,
                           save_only_single_checkpoint_file=config.train.save_only_single_checkpoint_file,
                           normalize_spectrograms=config.train.normalize_spectrograms,
                           use_train_subsets_from_previous_run=config.train.use_train_subsets_from_previous_run,
                           previous_run_path=config.train.previous_run_path,
                           root_results_dir=config.output.root_results_dir)

                # get config again
                # because learncurve changed results_dir_made_by_main_script
                config = vak.config.parse.parse_config(config_file)
                summary(results_dirname=config.output.results_dirname,
                        train_data_dict_path=config.train.train_data_dict_path,
                        networks=config.networks,
                        train_set_durs=config.train.train_set_durs,
                        num_replicates=config.train.num_replicates,
                        labelset=config.data.labelset,
                        test_data_dict_path=config.train.test_data_dict_path,
                        normalize_spectrograms=config.train.normalize_spectrograms)

        elif command == 'summary':
            summary(results_dirname=config.output.results_dirname,
                    train_data_dict_path=config.train.train_data_dict_path,
                    networks=config.networks,
                    train_set_durs=config.train.train_set_durs,
                    num_replicates=config.train.num_replicates,
                    labelset=config.data.labelset,
                    test_data_dict_path=config.train.test_data_dict_path,
                    normalize_spectrograms=config.train.normalize_spectrograms)

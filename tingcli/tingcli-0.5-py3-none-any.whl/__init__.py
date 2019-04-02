from .utils import *
import fire
import os
import shutil
from pathlib import Path
import re

PODFILE_PATH = './Podfile'
PODFILE_BAK_PATH = './.PodfileBak'
RNKIT_DEV_HEADER = './Pods/RNKit/RNKit/Classes/RNKitDev.h'

logger = create_logger()

class TingCli(object):
    def ipod(self, use_rn_source=False, use_xmlive_source=False, force_update_repo=False):
        self.__detect_and_update_repo(force_update_repo)
        self.__do_rnkit_clean(use_rn_source)
        self.__rewrite_podfile(use_rn_source)
        prefix_envs = ''
        if use_rn_source:
            prefix_envs += 'rnkit_source=1 experiment=1 '
        if use_xmlive_source:
            prefix_envs += 'XMLive_source=1 '
        os.system(prefix_envs + ' pod install --verbose')
        self.__restore_podfile(use_rn_source)

    def __detect_and_update_repo(self, force_update_repo=False):
        repos = self.__detect_pod_repos()
        logger.info('找到{0}个pod repo'.format(len(repos)))
        index = 1
        for repo in repos:
            logger.info('{0}. {1}'.format(index, repo))
            index += 1
        if len(repos) <= 0:
            return
        if not force_update_repo:
            result = input('选择要更新的repo序号，用逗号隔开（比如1,2）')
            indexes = result.strip(' ').split(',')
            if len(indexes) > 0:
                for index in indexes:
                    index_int = int(index.strip(' ')) - 1
                    if 0 <= index_int < len(repos):
                        os.system('pod repo update {0}'.format(repos[index_int]))
            else:
                logger.warn('你放弃了更新这些repo')
        else:
            logger.info('开始强制更新所有repo')
            for repo in repos:
                os.system('pod repo update {0}'.format(repo))

    def __detect_pod_repos(self):
        outputs = run_command('pod repo list')
        repos = []
        for line in outputs:
            line_str = str(line, 'utf8')
            result = re.match(r'^[a-zA-Z][a-zA-Z\-_0-9]*', line_str)
            if result:
                repos.append(line_str.strip('\n'))
        return repos

    def __restore_podfile(self, use_rn_source):
        if use_rn_source:
            logger.info('检测到使用RN源码pod install，即将恢复Podfile')
            if os.path.exists(PODFILE_BAK_PATH):
                os.remove(PODFILE_PATH)
                shutil.copy(PODFILE_BAK_PATH, PODFILE_PATH)
                os.remove(PODFILE_BAK_PATH)
                logger.info('恢复成功')
            else:
                logger.error('未检测到Podfile备份，恢复失败')

    def __rewrite_podfile(self, use_rn_source):
        if not use_rn_source:
            return
        logger.info('检测到使用RN源码pod install，即将修改Podfile')
        if os.path.exists(PODFILE_PATH):
            # backup Podfile
            logger.info('备份现有的Podfile')
            shutil.copy(PODFILE_PATH, PODFILE_BAK_PATH)
            logger.info('修改Podfile')
            with open(PODFILE_PATH, 'r+') as file:
                file.seek(0, os.SEEK_SET)
                lines = file.readlines()
                lines.insert(0, 'source "git@gitlab.ximalaya.com:react-native/rnspecs.git"\n')
                file.seek(0, os.SEEK_SET)
                file.writelines(lines)
                file.flush()

    def __do_rnkit_clean(self, use_rn_source):
        need_clean = False
        if use_rn_source and not os.path.exists(RNKIT_DEV_HEADER):
            need_clean = True
        if not use_rn_source and os.path.exists(RNKIT_DEV_HEADER):
            need_clean = True
        if os.path.exists('./Podfile.lock'):
            os.remove('./Podfile.lock')
        if need_clean:
            home = str(Path.home())
            logger.warn('检测当前Pod和环境不匹配，准备执行缓存清理操作')
            clean_paths = [
                './Pods/RNKit',
                '{0}/Library/Caches/CocoaPods/Pods/Release/RNKit/'.format(home),
                './Pods/XMHybrid',
                '{0}/Library/Caches/CocoaPods/Pods/Release/XMHybrid/'.format(home),
                './Pods/XMLive',
                '{0}/Library/Caches/CocoaPods/Pods/Release/XMLive/'.format(home)]
            for path in clean_paths:
                if os.path.exists(path):
                    logger.warn('开始清理：{0}'.format(path))
                    shutil.rmtree(path)



fire.Fire(TingCli)

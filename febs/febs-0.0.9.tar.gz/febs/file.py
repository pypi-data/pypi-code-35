#! /usr/bin/env python
# coding=utf-8
#================================================================
#   Copyright (C) 2019 BP Ltd. All rights reserved.
#
#   Author      : brainpoint
#   Created date: 2019-03-30 11:51
#   Description : 
#
#================================================================

import os
import platform
import re
import shutil

sepr = '/' if platform.system() == 'Windows' else '\\'


class file:

  @staticmethod
  def normalize(path):
      '''
      将路径分隔符号替换为当前系统正确的分隔符
      '''
      return path.replace(sepr, os.path.sep)

  @staticmethod
  def dirIsExist(dir):
      '''
      判断文件夹是否存在
      :param dir: 目录路径.
      :return bool
      '''
      if isinstance(dir, str):
          dir = os.path.realpath(dir.replace(sepr, os.path.sep))
          return os.path.isdir(dir)
      else:
          return False

  @staticmethod
  def dirAssure(dir):
      '''
      保证文件夹存在
      :return bool. 若不存在新建; 文件夹存在返回true.
      '''
      if not isinstance(dir, str) or dir == '':
          return True

      if file.dirIsExist(dir):
          return True

      dir = dir.replace(sepr, os.path.sep)
      dir = os.path.realpath(dir)

      ldir = len(dir)
      if dir[ldir-1] != os.sep:
          dir += os.sep
          ldir += 1

      j = 0
      paths = []
      for i in range(ldir):
          if dir[i] == os.sep and i != 0:
              paths.append(dir[j:i])
              j = i+1

      dir = ''
      for i in range(len(paths)):
          if i == 0:
              dir += paths[i]
          else:
              dir += os.sep + paths[i]

          if file.dirIsExist(dir):
              continue

          os.mkdir(dir)

      return False

  @staticmethod
  def dirCopy(src, dest, callback):
      '''
      copy directory
      :param callback: def callback(err) 如果发生错误, 将回调错误信息; 否则 err==None
      '''
      if src == None or dest == None or file.dirIsExist(src) == False:
          callback and (callback("dirCopy src or dest error; src: %s. dest: %s" %(src, dest)))
          return False

      src = src.replace(sepr, os.path.sep)
      src = os.path.realpath(src)

      dest = dest.replace(sepr, os.path.sep)
      dest = os.path.realpath(dest)

      arrFiles = []
      arrEmptyDirs = []

      def dirCopy1(dirSrc, dirDest, arrF):
          file.dirAssure(dirDest)
          src1 = None
          dest1 = None

          for i in range(len(arrF)):
              src1 = os.path.join(dirSrc, arrF[i])
              dest1 = os.path.join(dirDest, arrF[i])
              if os.path.isdir(src1):
                  arrF1 = os.listdir(src1)
                  if None == arrF1 or len(arrF1) == 0:
                      arrEmptyDirs.append(dest1)
                  else:
                      dirCopy1(src1, dest1, arrF1)
              else:
                  arrFiles.append(src1)
                  arrFiles.append(dest1)
      # function.

      arrF = os.listdir(src)
      if None == arrF or len(arrF) == 0:
          arrEmptyDirs.append(dest)
      else:
          dirCopy1(src, dest, arrF)

      # copy.
      for i in range(arrEmptyDirs):
          file.dirAssure(arrEmptyDirs[i])

      index = 0
      def copy1(err):
          if err:
              callback and callback(err)
              return

          nonlocal index
          if index < len(arrFiles):
              i1 = index; index = index+1
              i2 = index; index = index+1
              file.fileCopy(arrFiles[i1], arrFiles[i2], copy1)
          else:
              callback and callback(None)

      copy1(None)


  @staticmethod
  def dirRemoveRecursive(dir):
      '''
      删除文件夹
      :return bool 指明是否删除
      '''
      if not isinstance(dir, str):
          return False

      dir = dir.replace(sepr, os.path.sep)
      dir = os.path.realpath(dir)

      try:
          if dir and os.path.isdir(dir):
              fspath = None
              dirList = os.listdir(dir)
              for i in range(len(dirList)):
                  fspath = os.path.join(dir, dirList[i])
                  if os.path.isdir(fspath):
                      file.dirRemoveRecursive(fspath)
                  else:
                      os.remove(fspath)
              os.removedirs(dir)
          return True
      except BaseException:
          return False

  @staticmethod
  def dirExplorer(dir, pattern = None):
      '''
      获取当前目录下的子文件与子目录
      :param dir: 要搜索的目录路径
      :param pattern: 子文件或子目录名称,匹配的正则表达式
                      仅从名称的第一个字符开始匹配, 例如: r'a.*', 匹配 a开头的文件名.
      :return {files:[], dirs:[]}; 发生错误返回None.
      '''
      ret = {}
      ret['files'] = []
      ret['dirs'] = []
      fspath = None

      try:
          dir = dir.replace(sepr, os.path.sep)
          dir = os.path.realpath(dir)
          
          dirList = os.listdir(dir)
          for i in range(len(dirList)):
              if pattern:
                  pr = re.match(pattern, dirList[i])
                  if not pr:
                      continue
              
              fspath = os.path.join(dir, dirList[i])
              if os.path.isdir(fspath):
                  ret['dirs'].append(dirList[i])
              else:
                  ret['files'].append(dirList[i])
      except BaseException:
          return None

      return ret


  @staticmethod
  def dirExplorerFilesRecursive(dir, pattern = None):
      '''
      递归获取当前目录下的所有子文件
      :param dir: 要搜索的目录路径
      :param pattern: 子文件或子目录名称,匹配的正则表达式
                      仅从名称的第一个字符开始匹配, 例如: r'a.*', 匹配 a开头的文件名.
      :return list; 发生错误返回None.
      '''
      ret = []
      fspath = None

      dirs = []

      try:
          dir = dir.replace(sepr, os.path.sep)
          dir = os.path.realpath(dir)
          
          dirList = os.listdir(dir)
          for i in range(len(dirList)):
              fspath = os.path.join(dir, dirList[i])

              if os.path.isdir(fspath):
                  dirs.append(dirList[i])
              elif os.path.isfile(fspath):
                  if pattern:
                      pr = re.match(pattern, dirList[i])
                      if not pr:
                          continue
                  ret.append(dirList[i])

          j = 0
          while j < len(dirs):
              dirList = os.listdir(os.path.join(dir, dirs[j]))
              for i in range(len(dirList)):
                  fspath = os.path.join(dir, dirs[j], dirList[i])
                  if os.path.isdir(fspath):
                      dirs.append(os.path.join(dirs[j], dirList[i]))
                  elif os.path.isfile(fspath):
                      if pattern:
                          pr = re.match(pattern, dirList[i])
                          if not pr:
                              continue
                      ret.append(os.path.join(dirs[j], dirList[i]))
              j = j +1

      except BaseException as e:
          return None

      return ret

  @staticmethod
  def dirExplorerDirsRecursive(dir, pattern = None):
      '''
      递归获取当前目录下的所有子目录
      :param dir: 要搜索的目录路径
      :param pattern: 子文件或子目录名称,匹配的正则表达式
                      仅从名称的第一个字符开始匹配, 例如: r'a.*', 匹配 a开头的文件名.
      :return list; 发生错误返回None.
      '''
      ret = []
      fspath = None

      dirs = []

      try:
          dir = dir.replace(sepr, os.path.sep)
          dir = os.path.realpath(dir)
          
          dirList = os.listdir(dir)
          for i in range(len(dirList)):
              fspath = os.path.join(dir, dirList[i])

              if os.path.isdir(fspath):
                  dirs.append(dirList[i])
                  if pattern:
                      pr = re.match(pattern, dirList[i])
                      if not pr:
                          continue
                  ret.append(dirList[i])

          j = 0
          while j < len(dirs):
              dirList = os.listdir(os.path.join(dir, dirs[j]))
              for i in range(len(dirList)):
                  fspath = os.path.join(dir, dirs[j], dirList[i])
                  if os.path.isdir(fspath):
                      dirs.append(os.path.join(dirs[j], dirList[i]))
                      if pattern:
                          pr = re.match(pattern, dirList[i])
                          if not pr:
                              continue
                      ret.append(os.path.join(dirs[j], dirList[i]))
              j = j +1

      except BaseException:
          return None

      return ret

  @staticmethod
  def fileSize(file):
      '''
      获得文件的字节大小
      :return number.-1表示错误
      '''
      if not isinstance(file, str) or file == '':
          return -1

      file = file.replace(sepr, os.path.sep)
      file = os.path.realpath(file)
                
      if os.path.isfile(file):
          size = os.path.getsize(file)
          return size
      
      return -1

  @staticmethod
  def fileIsExist(file):
      '''
      判断文件是否存在
      :return bool
      '''
      if not isinstance(file, str) or file == '':
          return False
      
      file = file.replace(sepr, os.path.sep)
      file = os.path.realpath(file)

      return os.path.isfile(file)

  @staticmethod
  def fileCopy(src, dest, callback):
      '''
      复制文件
      :param callback: (err) => {}, 执行此函数时表示复制完成.
      :return bool 指明是否成功
      '''
      if not isinstance(src, str) or not isinstance(dest, str):
          callback and callback('fileCopy src or dest error; src: %s. dest: %s ' %(src, dest))
          return False

      src = src.replace(sepr, os.path.sep)
      src = os.path.realpath(src)

      dest = dest.replace(sepr, os.path.sep)
      dest = os.path.realpath(dest)

      if not os.path.isfile(src) or os.path.isfile(dest):
          callback and callback('fileCopy src or dest error; src: %s. dest: %s ' %(src, dest))
          return False

      if os.path.isdir(src):
          callback and callback('src is directory')
          return False

      file.dirAssure(os.path.dirname(dest))

      try:
          shutil.copyfile(src, dest)
      except BaseException:
          return False
      
      callback and callback(None)
      return True

  @staticmethod
  def fileRemove(file):
      '''
      移除文件
      :return bool 指明是否删除
      '''
      if not isinstance(file, str):
          return False

      file = file.replace(sepr, os.path.sep)
      file = os.path.realpath(file)
      
      try:
          if os.path.isfile(file):
              os.remove(file)
              return True
      except BaseException:
          return False
      
      return True

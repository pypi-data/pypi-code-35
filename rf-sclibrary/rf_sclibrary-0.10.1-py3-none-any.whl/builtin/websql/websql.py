import requests
import urllib.parse
import re
import json
import sys
from .crpt import SHA1, bytes2hex, rc4_arr, utf2bytes, bytes2utf, hex2bytes

from robot.api import logger

class WebSQL(object):
  url = 'https://mysqlweb.souche-inc.com/dbninja/'
  url_data = '%sdata.php' % url

  def __init__(self, uname, passwd):
    super().__init__()
    self.key = passwd
    pwd = SHA1(self.key)
    self.session = self.login_for_session(uname, pwd)

  def login_for_session(self, user_name, passwd):
    ''' 登录获取 session '''
    try:
      data = { 'uname': user_name, 'passwd': passwd }
      r_login = requests.post(self.url, data=data)
      return r_login.headers.get('Set-Cookie')
    except Exception as e:
      logger.error(e)
      sys.exit(1)

  def get_dbs(self):
    ''' 获取数据库 '''
    try:
      headers = { 'cookie': self.session }
      request_body = '{"action":"load_config"}'
      r_dbs = requests.post(self.url_data, headers=headers, data=self.encry(request_body))
      text_dbs = self.decry(r_dbs.text)
      json_dbs = json.loads(text_dbs)
      dbs = []
      for host in json_dbs.get('hosts'):
        dbs.append({'cid': host['cid'], 'host' : host['label']})
      return dbs
    except Exception as e:
      logger.error(e)
      sys.exit(1)

  def find_db(self, host_label, db):
    dbs = self.get_dbs()
    for item in dbs:
      if item.get('host') == host_label:
        return item.get('cid')
    return None

  def query(self, host_label, db, sql):
    # 查询目标数据库的cid
    cid = self.find_db(host_label, db)
    if cid == None:
      logger.error("WebSQL中无法找到该数据库信息")
      sys.exit(1)

    # 根据sql查询fields, pageCount, outFile
    headers = { 'cookie': '%s;sql_commandEditor=%s' % (self.session, urllib.parse.quote(sql))}
    request_body ='{"action":"query","cid":"%s","db":"%s","query":"%s","params":[],"flags":5,"toFile":false,"limited":true}' % (cid, db, sql)
    r_outfile = requests.post(self.url_data, headers = headers, data = self.encry(request_body))
    if r_outfile.text[0:2] == "!:":
      text = self.decry(r_outfile.text)
      result = json.loads(text)
      fields, page_count, out_file = self.parse_fields(result)
      if page_count > 1:
        logger.warn("查询结果大于100, 返回100个结果（一共%s页）" % page_count)
      # 根据outfile查询结果
      request_body = '{"action":"get_query_result","file":"%s","result":0,"page":0}' % (out_file)
      r_result = requests.post(self.url_data, headers = headers, data = self.encry(request_body))
      if r_result.text[0:2] == "!:":
        text = self.decry(r_result.text)
        result = json.loads(text.replace(',\n];', ']'))
        return self.format_result(fields, result)
  
  def encry(self, data):
    return '!:' + bytes2hex(rc4_arr(self.key, utf2bytes(data)))

  def decry(self, data):
    if data[0:2] == "!:":
      text = bytes2utf(rc4_arr(self.key, hex2bytes(data[2:])))
      self.key = re.findall(r'^\!\:(\w+)\n', text)[0]
      text = text[2+len(self.key):]
      return text
    logger.error('返回异常，不包含 !: 加密数据')
    sys.exit(1)

  def parse_fields(self, result):
    data = result.get('results')[0]
    fields = data.get('fields')
    db_fields = []
    for f in fields:
      db_fields.append(f.get('field'))
    page_count = data.get('pageCount')
    out_file = result.get('outFile')
    return db_fields, page_count, out_file

  def format_result(self, fields, result):
    array = []
    for i in range(len(result)):
      item = dict()
      for j in range(len(fields)):
        item[fields[j]] = result[i][j]
      array.append(item)
    return array
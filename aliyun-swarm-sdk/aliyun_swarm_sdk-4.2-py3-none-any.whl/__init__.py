#coding: utf8
import requests
import json

class Swarm_Object(object):
    """swarm 应用管理"""
    def create_application(cluster_address, ca_pem_path, cert_pem_path, key_pem_path, data):
        """创建swarm应用"""
        cluster_address += "/projects/"
        try:
            res = requests.post(cluster_address, verify=ca_pem_path, cert=(cert_pem_path, key_pem_path), json=data)
            if res.status_code == 201:
                msg = {'status': 200, 'msg': 'swarm 应用创建成功'}
            else:
                res_str = str(res.content, "utf-8")
                res_dict = json.loads(res_str)
                msg = {'status': 500, 'msg': 'swarm 应用创建失败,%s' % res_dict['message']}
        except Exception as e:
            msg = {'status': 500, 'msg': '集群地址 %s 调用创建接口失败,请联系管理员!' % cluster_address}
        print(msg)
        return msg

    def update_application(cluster_address, ca_pem_path, cert_pem_path, key_pem_path, data, name):
        """ 更新应用|蓝绿更新应用"""
        cluster_address += "/projects/" + name + "/update"
        try:
            res = requests.post(cluster_address, verify=ca_pem_path, cert=(cert_pem_path, key_pem_path), json=data)
            if res.status_code == 202:
                msg = {'status': 200, 'msg': '应用 %s 更新成功' % name}
            else:
                res_str = str(res.content, "utf-8")
                res_dict = json.loads(res_str)
                msg = {'status': 500, 'msg': '应用 %s 更新失败,%s' % (name, res_dict['message'])}
        except Exception as e:
            msg = {'status': 500, 'msg': '集群地址 %s 调用更新接口失败,请联系管理员!' % cluster_address}
        print(msg)
        return msg

    def update_confirmation(cluster_address, ca_pem_path, cert_pem_path, key_pem_path, name):
        """ 更新应用确认"""
        cluster_address += "/projects/" + name + "/confirm-update?force=true"
        try:
            res = requests.post(cluster_address, verify=ca_pem_path, cert=(cert_pem_path, key_pem_path))
            if res.status_code == 200:
                msg = {'status': 200, 'msg': '应用 %s 发布确认成功' % name}
            else:
                msg = {'status': 500, 'msg': '应用 %s 发布确认失败' % name}
        except Exception as e:
            msg = {'status': 500, 'msg': '集群地址 %s 调用更新确认接口失败,请联系管理员!' % cluster_address}
        print(msg)
        return msg

    def redeploy_application(cluster_address, ca_pem_path, cert_pem_path, key_pem_path, name):
        """ 重新部署应用"""
        cluster_address += "/projects/" + name + "/redeploy"
        try:
            res = requests.post(cluster_address, verify=ca_pem_path, cert=(cert_pem_path, key_pem_path))
            if res.status_code == 202:
                msg = {'status': 200, 'msg': '应用 %s 重新部署成功' % name}
            else:
                msg = {'status': 500, 'msg': '应用 %s 重新部署失败' % name}
        except Exception as e:
            msg = {'status': 500, 'msg': '集群地址 %s 调用重新部署接口失败,请联系管理员!' % cluster_address}
        print(msg)
        return msg

    def stop_application(cluster_address, ca_pem_path, cert_pem_path, key_pem_path, name):
        """ 停止应用"""
        cluster_address += "/projects/" + name + "/stop"
        try:
            res = requests.post(cluster_address, verify=ca_pem_path, cert=(cert_pem_path, key_pem_path))
            if res.status_code == 200:
                msg = {'status': 200, 'msg': '应用 %s 停止成功' % name}
            else:
                msg = {'status': 500, 'msg': '应用 %s 停止失败' % name}
        except Exception as e:
            msg = {'status': 500, 'msg': '集群地址 %s 调用停止应用接口失败,请联系管理员!' % cluster_address}
        print(msg)
        return msg

    def start_application(cluster_address, ca_pem_path, cert_pem_path, key_pem_path, name):
        """ 启动应用"""
        cluster_address += "/projects/" + name + "/start"
        try:
            res = requests.post(cluster_address, verify=ca_pem_path, cert=(cert_pem_path, key_pem_path))
            if res.status_code == 200:
                msg = {'status': 200, 'msg': '应用 %s 启动成功' % name}
            else:
                msg = {'status': 500, 'msg': '应用 %s 启动失败' % name}
        except Exception as e:
            msg = {'status': 500, 'msg': '集群地址 %s 调用停止应用接口失败,请联系管理员!' % cluster_address}
        print(msg)
        return msg

    def kill_application(cluster_address, ca_pem_path, cert_pem_path, key_pem_path, name):
        """ 终止应用"""
        cluster_address += "/projects/" + name + "/kill"
        try:
            res = requests.post(cluster_address, verify=ca_pem_path, cert=(cert_pem_path, key_pem_path))
            if res.status_code == 200:
                msg = {'status': 200, 'msg': '应用 %s 终止成功' % name}
            else:
                msg = {'status': 500, 'msg': '应用 %s 终止失败' % name}
        except Exception as e:
            msg = {'status': 500, 'msg': '集群地址 %s 调用终止应用接口失败,请联系管理员!' % cluster_address}
        print(msg)
        return msg

    def delete_application(cluster_address, ca_pem_path, cert_pem_path, key_pem_path, name):
        """ 删除应用"""
        cluster_address += "/projects/" + name + "?force=true&volume=true"
        try:
            res = requests.delete(cluster_address, verify=ca_pem_path, cert=(cert_pem_path, key_pem_path))
            if res.status_code == 200:
                msg = {'status': 200, 'msg': '应用 %s 删除成功' % name}
            else:
                msg = {'status': 500, 'msg': '应用 %s 删除失败' % name}
        except Exception as e:
            msg = {'status': 500, 'msg': '集群地址 %s 调用删除应用接口失败,请联系管理员!' % cluster_address}
        print(msg)
        return msg

import unittest



class TaskByNameFromPlaybookTestCase(unittest.TestCase):
    spec = """name: install ingress-nginx (ServiceAccount)
    tags:
    - ansible.cochise.io/task-impl:qsa.ext.k8s.tasks.KubernetesServiceAccountTask
    - app.kubernetes.io/part-of:ingress-nginx
    - deployment.cochise.io/env:global
    - kubernetes.io/resource-type:serviceaccount
    - meta.cochise.io/namespace:k8s.iam
    - meta.cochise.io/qualname:k8s.iam.nginx-ingress-serviceaccount
    - meta.cochise.io/version:1.0
   """


if __name__ == '__main__':
    unittest.main()

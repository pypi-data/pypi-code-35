import networkx as nx
import requests
from time import sleep
from itertools import permutations
from itertools import combinations
from collections import defaultdict








class Information(object):
    def __init__(self):
        self.pool = {}
        self.little_pool = {}
        self.big_pool = {}
        self.best_city = [0,0]
        self.best_home = [0,0]
        self.best_school = [0,0]
        self.best_university = [0,0]
        self.best_year = [0,0]
        self.best_work = [0,0]


    def getInfo(self,nodes,MY_USER_ID,TOKEN):
        res = []
        for i in range(0, len(nodes), 200):
            ids = ""
            if (i < len(nodes) - 200):
                for j in range(i, i + 200):
                    ids = ids + str(nodes[j]) + ','
                sleep(0.5)
                getInf = requests.get(
                    'https://api.vk.com/method/users.get?user_ids=' + ids + '&fields=city,home_town,bdate,schools,universities,career&version=5.92&access_token=' + TOKEN)
                res.extend(getInf.json()['response'])
            else:
                for j in range(i, len(nodes)):
                    ids = ids + str(nodes[j]) + ','
                sleep(0.5)
                getInf = requests.get(
                    'https://api.vk.com/method/users.get?user_ids=' + ids + '&fields=city,home_town,bdate,schools,universities,career&version=5.92&access_token=' + TOKEN)
                res.extend(getInf.json()['response'])
        city = []
        home_town = []
        university = []
        schools = []
        years = []
        work = []
        for id_inf in res:
            city.append(id_inf.get('city'))
            home_town.append(id_inf.get('home_town'))
            if (id_inf.get('universities')):
                tmp = '' + str(id_inf.get('universities')[0].get('name'))+' ' + str(id_inf.get('universities')[0].get('faculty_name')) #+' '+str(id_inf.get('universities')[0].get('education_status'))#+' '+ str(id_inf.get('universities')[0].get('chair_name'))
                university.append(tmp)
            if (id_inf.get('schools')):
                tmp = '' + str(id_inf.get('schools')[0].get('name'))
                schools.append(tmp)
            if (id_inf.get('bdate')):
                if (len(id_inf.get('bdate'))>7):
                    years.append(id_inf.get('bdate')[-4:])
            if (id_inf.get('career')):
                tmp = '' + str(id_inf.get('career')[0].get('company'))
                work.append(tmp)
        city_set = set(city)
        city_set.discard(None)
        max_city_id = 0
        max_city_count = 0
        for city_id in city_set:
            if (city.count(city_id)>max_city_count):
                max_city_count = city.count(city_id)
                max_city_id = city_id
        metric = max_city_count/len(res)
        if (self.best_city[1]<metric):
            self.best_city[0] = max_city_id
            self.best_city[1] = metric

        home_town_set = set(home_town)
        home_town_set.discard('')
        home_town_set.discard(None)
        max_home_town_id = 0
        max_home_town_count = 0
        for home_town_id in home_town_set:
            if (home_town.count(home_town_id)>max_home_town_count):
                max_home_town_count = home_town.count(home_town_id)
                max_home_town_id = home_town_id
        metric = max_home_town_count/len(res)
        if (self.best_home[1]<metric):
            self.best_home[0] = max_home_town_id
            self.best_home[1] = metric


        university_set = set(university)
        max_university_id = 0
        max_university_count = 0
        for university_id in university_set:
            if(university.count(university_id)>max_university_count):
                max_university_count = university.count(university_id)
                max_university_id = university_id
        metric = max_university_count/len(res)
        if (self.best_university[1]<metric):
            self.best_university[0] = max_university_id
            self.best_university[1] = metric

        schools_set = set(schools)
        max_school_id = 0
        max_school_count = 0
        for school_id in schools_set:
            if(schools.count(school_id)>max_school_count):
                max_school_count = schools.count(school_id)
                max_school_id = school_id
        metric = max_school_count/len(res)

        if (self.best_school[1]<metric):
            self.best_school[0] = max_school_id
            self.best_school[1] = metric

        years_set = set(years)

        max_year_id = 0
        max_year_count = 0
        for years_id in years_set:
            if(years.count(years_id)>max_year_count):
                max_year_count = years.count(years_id)
                max_year_id = years_id
        metric = max_year_count/len(res)
        if (self.best_year[1]<metric):
            self.best_year[0]=max_year_id
            self.best_year[1]=metric

        work_set = set(work)
        work_set.discard('None')
        max_work_id=0
        max_work_count=0
        for work_id in work_set:
            if (work.count(work_id)>max_work_count):
                max_work_count=work.count(work_id)
                max_work_id=work_id
        metric = max_work_count/len(res)
        if (self.best_work[1]<metric):
            self.best_work[0]=max_work_id
            self.best_work[1]=metric

    def getUserFriends(self,MY_USER_ID,TOKEN):
        r = requests.get('https://api.vk.com/method/friends.get?user_id='+str(MY_USER_ID)+'&version=5.92&access_token='+TOKEN)
        response_data = r.json()['response']
        return response_data

    def split(self,fr_str,pool,MY_USER_ID,TOKEN):

        for i in range(0,len(fr_str),25):
            part = ""
            temp = list()
            if (i<len(fr_str)-25):
                for j in range(i,i+25):
                    part = part + str(fr_str[j]) + ','
                    temp.append(fr_str[j])

                sleep(0.3)
                r = requests.get('https://api.vk.com/method/execute.getFriends?targets=' + part + '&version=5.92&access_token=' + TOKEN)
                resp = r.json()['response']


                for k in range(0, len(resp)):
                    if not (temp[k] in pool):
                        pool[temp[k]] = resp[k]

            else:
                for j in range(i,len(fr_str)):
                    part = part + str(fr_str[j]) + ','
                    temp.append(fr_str[j])
                sleep(0.3)
                r = requests.get('https://api.vk.com/method/execute.getFriends?targets='+part+'&version=5.92&access_token='+TOKEN)
                resp = r.json()['response']


                for k in range(0,len(resp)):
                    if not (temp[k] in pool):
                        pool[temp[k]] = resp[k]


    def makeEdges(self,nodes,pool,g):
        for node in nodes:
            for key in pool:
                if (pool.get(key)!=0):
                    if (pool.get(key).count(node)!=0):
                        g.add_edge(node,key,weight=1.)

    def publicInformation(self,MY_USER_ID,TOKEN):
        getInf = requests.get(
            'https://api.vk.com/method/users.get?user_ids=' + str(
                MY_USER_ID) + '&fields=city,home_town,bdate,schools,universities,career&version=5.92&access_token=' + TOKEN)
        user_info = getInf.json()['response']
        print("Указаны явно: ")
        print("Имя и фамилия: " +user_info[0]['first_name'] + ' ' + user_info[0]['last_name'])

        if (user_info[0].get('city')):
            r = requests.get('https://api.vk.com/method/database.getCitiesById?city_ids=' + str(user_info[0]['city']) + '&version=5.92&access_token=' + TOKEN)
            resp = r.json()['response']
            print("Город: " + resp[0]['name'])

        if (user_info[0].get('home_town')):
            print("Родной город: " + user_info[0]['home_town'])
        if (user_info[0].get('schools')):
            for i in range(0,len(user_info[0].get('schools'))):
                print("Школа: " + user_info[0].get('schools')[i].get('name'))
        if (user_info[0].get('universities')):
            for i in range(0,len(user_info[0].get('universities'))):
                print("Университет: " + user_info[0].get('universities')[i].get('name') + ' ' + user_info[0].get('universities')[i].get('faculty_name'))
        if (user_info[0].get('bdate')):
            print("Дата рождения: " + user_info[0]['bdate'])
        if (user_info[0].get('career')):
            print("Работа: " + user_info[0]['career'])

    def expressAnalyse(self,MY_USER_ID,TOKEN):

        resp = self.getUserFriends(MY_USER_ID,TOKEN)
        self.publicInformation(MY_USER_ID,TOKEN)
        nodes = list(resp)
        g = nx.Graph()
        for fr in resp:
            g.add_edge(MY_USER_ID, fr, weight=1.)
        self.split(resp,self.pool,MY_USER_ID,TOKEN)
        self.makeEdges(nodes, self.pool, g)
        louvain = Louvain()
        partition = louvain.getBestPartition(g)
        p = defaultdict(list)
        for node, com_id in partition.items():
            p[com_id].append(node)

        for com, nodes in p.items():
            self.getInfo(nodes,MY_USER_ID,TOKEN)

        r = requests.get('https://api.vk.com/method/database.getCitiesById?city_ids=' + str(
            self.best_city[0]) + '&version=5.92&access_token=' + TOKEN)
        resp = r.json()['response']
        print('\n')
        print('Предположение: (* - достовеность информации мала)')
        #print('* - достовеность информации мала')
        if (self.best_city[1]<0.1):
            print('Город: ' + resp[0]['name'] +' *')
        else:
            print('Город: ' + resp[0]['name'])
        if (self.best_home[1]<0.1):
            print('Родной город: ' + self.best_home[0] + ' *')
        else:
            print('Родной город: '+ self.best_home[0])
        if (self.best_school[1]<0.1):
            print('Школа: ' + self.best_school[0] + ' *')
        else:
            print('Школа: ' + self.best_school[0])
        if (self.best_university[1]<0.1):
            print('Университет: ' + self.best_university[0] + ' *')
        else:
            print('Университет: ' + self.best_university[0])
        if (self.best_year[1]<0.1):
            print('Год рождения: ' + self.best_year[0]+ ' *')
        else:
            print('Год рождения: ' + self.best_year[0])
        if (self.best_work[1]<0.1):
            print('Работа: ' + self.best_work[0]+ ' *')
        else:
            print('Работа: ' + self.best_work[0])

    def deepAnalyse(self,MY_USER_ID,TOKEN):
        resp = self.getUserFriends(MY_USER_ID,TOKEN)
        self.publicInformation(MY_USER_ID, TOKEN)
        g = nx.Graph()
        for fr in resp:
            g.add_edge(MY_USER_ID, fr, weight=1.)
        self.split(resp, self.little_pool,MY_USER_ID,TOKEN)
        self.big_pool.update(self.little_pool)
        for key in self.little_pool:
            if (self.little_pool.get(key)!=0):
                self.split(self.little_pool.get(key), self.big_pool,MY_USER_ID,TOKEN)
        nodes = list(self.big_pool.keys())
        self.makeEdges(nodes, self.big_pool, g)
        louvain = Louvain()
        partition = louvain.getBestPartition(g)
        p = defaultdict(list)
        for node, com_id in partition.items():
            p[com_id].append(node)
        for com, nodes in p.items():
            self.getInfo(nodes,MY_USER_ID,TOKEN)

        r = requests.get('https://api.vk.com/method/database.getCitiesById?city_ids=' + str(
            self.best_city[0]) + '&version=5.92&access_token=' + TOKEN)
        resp = r.json()['response']
        print('\n')
        print('Предположение: (* - достовеность информации мала)')
        # print('* - достовеность информации мала')
        if (self.best_city[1] < 0.1):
            print('Город: ' + resp[0]['name'] + ' *')
        else:
            print('Город: ' + resp[0]['name'])
        if (self.best_home[1] < 0.1):
            print('Родной город: ' + self.best_home[0] + ' *')
        else:
            print('Родной город: ' + self.best_home[0])
        if (self.best_school[1] < 0.1):
            print('Школа: ' + self.best_school[0] + ' *')
        else:
            print('Школа: ' + self.best_school[0])
        if (self.best_university[1] < 0.1):
            print('Университет: ' + self.best_university[0] + ' *')
        else:
            print('Университет: ' + self.best_university[0])
        if (self.best_year[1] < 0.1):
            print('Год рождения: ' + self.best_year[0] + ' *')
        else:
            print('Год рождения: ' + self.best_year[0])
        if (self.best_work[1] < 0.1):
            print('Работа: ' + self.best_work[0] + ' *')
        else:
            print('Работа: ' + self.best_work[0])

class Louvain(object):
    def __init__(self):
        self.MIN_VALUE = 0.0000001
        self.node_weights = {}

    @classmethod
    def convertIGraphToNxGraph(cls, igraph):
        node_names = igraph.vs["name"]
        edge_list = igraph.get_edgelist()
        weight_list = igraph.es["weight"]
        node_dict = defaultdict(str)

        for idx, node in enumerate(igraph.vs):
            node_dict[node.index] = node_names[idx]

        convert_list = []
        for idx in range(len(edge_list)):
            edge = edge_list[idx]
            new_edge = (node_dict[edge[0]], node_dict[edge[1]], weight_list[idx])
            convert_list.append(new_edge)

        convert_graph = nx.Graph()
        convert_graph.add_weighted_edges_from(convert_list)
        return convert_graph

    def updateNodeWeights(self, edge_weights):
        node_weights = defaultdict(float)
        for node in edge_weights.keys():
            node_weights[node] = sum([weight for weight in edge_weights[node].values()])
        return node_weights

    def getBestPartition(self, graph, param=1.):
        node2com, edge_weights = self._setNode2Com(graph)

        node2com = self._runFirstPhase(node2com, edge_weights, param)
        best_modularity = self.computeModularity(node2com, edge_weights, param)

        partition = node2com.copy()
        new_node2com, new_edge_weights = self._runSecondPhase(node2com, edge_weights)

        while True:
            new_node2com = self._runFirstPhase(new_node2com, new_edge_weights, param)
            modularity = self.computeModularity(new_node2com, new_edge_weights, param)
            if abs(best_modularity - modularity) < self.MIN_VALUE:
                break
            best_modularity = modularity
            partition = self._updatePartition(new_node2com, partition)
            _new_node2com, _new_edge_weights = self._runSecondPhase(new_node2com, new_edge_weights)
            new_node2com = _new_node2com
            new_edge_weights = _new_edge_weights
        return partition

    def computeModularity(self, node2com, edge_weights, param):
        q = 0
        all_edge_weights = sum(
            [weight for start in edge_weights.keys() for end, weight in edge_weights[start].items()]) / 2

        com2node = defaultdict(list)
        for node, com_id in node2com.items():
            com2node[com_id].append(node)

        for com_id, nodes in com2node.items():
            node_combinations = list(combinations(nodes, 2)) + [(node, node) for node in nodes]
            cluster_weight = sum([edge_weights[node_pair[0]][node_pair[1]] for node_pair in node_combinations])
            tot = self.getDegreeOfCluster(nodes, node2com, edge_weights)
            q += (cluster_weight / (2 * all_edge_weights)) - param * ((tot / (2 * all_edge_weights)) ** 2)
        return q

    def getDegreeOfCluster(self, nodes, node2com, edge_weights):
        weight = sum([sum(list(edge_weights[n].values())) for n in nodes])
        return weight

    def _updatePartition(self, new_node2com, partition):
        reverse_partition = defaultdict(list)
        for node, com_id in partition.items():
            reverse_partition[com_id].append(node)

        for old_com_id, new_com_id in new_node2com.items():
            for old_com in reverse_partition[old_com_id]:
                partition[old_com] = new_com_id
        return partition

    def _runFirstPhase(self, node2com, edge_weights, param):
        all_edge_weights = sum(
            [weight for start in edge_weights.keys() for end, weight in edge_weights[start].items()]) / 2
        self.node_weights = self.updateNodeWeights(edge_weights)
        status = True
        while status:
            statuses = []
            for node in node2com.keys():
                statuses = []
                com_id = node2com[node]
                neigh_nodes = [edge[0] for edge in self.getNeighborNodes(node, edge_weights)]

                max_delta = 0.
                max_com_id = com_id
                communities = {}
                for neigh_node in neigh_nodes:
                    node2com_copy = node2com.copy()
                    if node2com_copy[neigh_node] in communities:
                        continue
                    communities[node2com_copy[neigh_node]] = 1
                    node2com_copy[node] = node2com_copy[neigh_node]

                    delta_q = 2 * self.getNodeWeightInCluster(node, node2com_copy, edge_weights) - (
                                self.getTotWeight(node, node2com_copy, edge_weights) * self.node_weights[
                            node] / all_edge_weights) * param
                    if delta_q > max_delta:
                        max_delta = delta_q
                        max_com_id = node2com_copy[neigh_node]

                node2com[node] = max_com_id
                statuses.append(com_id != max_com_id)

            if sum(statuses) == 0:
                break

        return node2com

    def _runSecondPhase(self, node2com, edge_weights):
        com2node = defaultdict(list)

        new_node2com = {}
        new_edge_weights = defaultdict(lambda: defaultdict(float))

        for node, com_id in node2com.items():
            com2node[com_id].append(node)
            if com_id not in new_node2com:
                new_node2com[com_id] = com_id

        nodes = list(node2com.keys())
        node_pairs = list(permutations(nodes, 2)) + [(node, node) for node in nodes]
        for edge in node_pairs:
            new_edge_weights[new_node2com[node2com[edge[0]]]][new_node2com[node2com[edge[1]]]] += edge_weights[edge[0]][
                edge[1]]
        return new_node2com, new_edge_weights

    def getTotWeight(self, node, node2com, edge_weights):
        nodes = [n for n, com_id in node2com.items() if com_id == node2com[node] and node != n]

        weight = 0.
        for n in nodes:
            weight += sum(list(edge_weights[n].values()))
        return weight

    def getNeighborNodes(self, node, edge_weights):
        if node not in edge_weights:
            return 0
        return edge_weights[node].items()

    def getNodeWeightInCluster(self, node, node2com, edge_weights):
        neigh_nodes = self.getNeighborNodes(node, edge_weights)
        node_com = node2com[node]
        weights = 0.
        for neigh_node in neigh_nodes:
            if node_com == node2com[neigh_node[0]]:
                weights += neigh_node[1]
        return weights

    def _setNode2Com(self, graph):
        node2com = {}
        edge_weights = defaultdict(lambda: defaultdict(float))
        for idx, node in enumerate(graph.nodes()):
            node2com[node] = idx
            for edge in graph[node].items():
                edge_weights[node][edge[0]] = edge[1]["weight"]
        return node2com, edge_weights
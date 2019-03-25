# -*- coding: utf-8 -*-
"""
纯蒙特卡罗树搜索（MCTS）的实现
A pure implementation of the Monte Carlo Tree Search (MCTS)
"""

import numpy as np
import copy
from operator import itemgetter


class TreeNode(object):
    """MCTS树中的节点类。 每个节点跟踪其自身的值Q，先验概率P及其访问次数调整的先前得分u。"""

    def __init__(self, parent, prior_p):
        self._parent = parent
        self._children = {}  # a map from action to TreeNode
        self._Q = 0         #节点分数，用于mcts树初始构建时的充分打散（每次叶子节点被最优选中时，节点隔级-leaf_value逻辑，以避免构建树时某分支被反复选中）
        self._n_visits = 0  #节点被最优选中的次数，用于树构建完毕后的走子选择
        self._u = 0
        self._P = prior_p   #action概率

    def expand(self, action_priors):
        """把策略函数返回的[(action,概率)]列表追加到child节点上
            Params：action_priors=走子策略函数返回的走子概率列表[(action,概率)]
        """
        for action, prob in action_priors:
            if action not in self._children:
                self._children[action] = TreeNode(self, prob)

    def select(self, c_puct):
        """从child中选择最大action Q+奖励u(P) 的动作
            Params：c_puct=child搜索深度
            Return: (action, next_node)
        """
        return max(self._children.items(), key=lambda act_node: act_node[1].get_value(c_puct))

    def get_value(self, c_puct):
        """计算并返回当前节点的值
            c_puct:     child搜索深度
            self._P:    action概率
            self._parent._n_visits  父节点的最优选次数
            self._n_visits          当前节点的最优选次数
            self._Q                 当前节点的分数，用于mcts树初始构建时的充分打散
        """
        self._u = (c_puct * self._P * np.sqrt(self._parent._n_visits) / (1 + self._n_visits))
        return self._Q + self._u

    def update(self, leaf_value):
        """更新当前节点的访问次数和叶子节点评估结果
            leaf_value: 从当前玩家的角度看子树的评估值.
        """
        # 访问计数
        self._n_visits += 1
        # Update Q, a running average of values for all visits.
        self._Q += 1.0*(leaf_value - self._Q) / self._n_visits

    def update_recursive(self, leaf_value):
        """同update(), 但是对所有祖先进行递归应用
            注意：这里递归-leaf_value用于mcts的充分打散，因为是随机，所以应尽量避免某分支被反复选中
        """
        # 非root节点时递归update祖先
        if self._parent:
            self._parent.update_recursive(-leaf_value)
        self.update(leaf_value)

    def is_leaf(self):
        """检查当前是否叶子节点"""
        return self._children == {}

    def is_root(self):
        """检查当前是否root节点"""
        return self._parent is None


class MCTS(object):
    """蒙特卡罗树搜索的简单实现"""

    def __init__(self, policy_value_fn, c_puct=5, n_playout=10000):
        """初始化参数"""
        self._root = TreeNode(None, 1.0)   #root
        self._policy = policy_value_fn  #可走子action及对应概率
        self._c_puct = c_puct           #MCTS child搜索深度
        self._n_playout = n_playout     #构建纯MCTS初始树的随机走子步数

    def get_move(self, state):
        """
        构建纯MCTS初始树(节点分布充分)，并返回child中访问量最大的action
            state: 当前游戏盘面
            Return: 构建的树中访问量最大的action
        """
        for n in range(self._n_playout):
            state_copy = copy.deepcopy(state)
            self._playout(state_copy)
        return max(self._root._children.items(), key=lambda act_node: act_node[1]._n_visits)[0]

    def _playout(self, state):
        """
        执行一步随机走子，对应一次MCTS树持续构建过程（选择最优叶子节点->根据走子策略概率扩充mcts树->评估并更新树的最优选次数）
            Params：state盘面 构建过程中会模拟走子，必须传入盘面的copy.deepcopy副本
        """
        node = self._root
        # 找到最优叶子节点：递归从child中选择并执行最大 动作Q+奖励u(P) 的动作
        while(1):
            if node.is_leaf():
                break
            # 从child中选择最优action
            action, node = node.select(self._c_puct)
            # 执行action走子
            state.do_move(action)

        # 走子策略返回的[(action,概率)]list
        action_probs, _ = self._policy(state)
        # 检查游戏是否有赢家
        end, winner = state.game_end()
        if not end: #没有结束时，把走子策略返回的[(action,概率)]list加载到mcts树child中
            node.expand(action_probs)
        # 使用快速随机走子评估此叶子节点继续往后走的胜负（state执行快速走子）
        leaf_value = self._evaluate_rollout(state)
        # 递归更新当前节点及所有父节点的最优选中次数和Q分数（最优选中次数是累加的，Q分数递归-1的目的在于避免构建初始mcts树时某分支被反复选中）
        node.update_recursive(-leaf_value)

    def update_with_move(self, last_move):
        """根据action更新根节点"""
        if last_move in self._root._children:
            self._root = self._root._children[last_move]
            self._root._parent = None
        else:
            self._root = TreeNode(None, 1.0)

    def _evaluate_rollout(self, state, limit=1000):
        """使用随机快速走子策略评估叶子节点
            Params：
                state 当前盘面
                limit 随机走子次数
            Return：如果当前玩家获胜返回+1
                    如果对手获胜返回-1
                    如果平局返回0
        """
        player = state.get_current_player()
        for i in range(limit):  #随机快速走limit次，用于快速评估当前叶子节点的优略
            end, winner = state.game_end()
            if end:
                break
            #给棋盘所有可落子位置随机分配概率，并取其中最大概率的action移动
            action_probs = MCTS.rollout_policy_fn(state)
            max_action = max(action_probs, key=itemgetter(1))[0]
            state.do_move(max_action)
        else:
            # If no break from the loop, issue a warning.
            print("WARNING: rollout reached move limit")
        if winner == -1:  # tie平局
            return 0
        else:
            return 1 if winner == player else -1

    @staticmethod
    def rollout_policy_fn(board):
        """给棋盘所有可落子位置随机分配概率"""
        action_probs = np.random.rand(len(board.availables))
        return zip(board.availables, action_probs)

    @staticmethod
    def policy_value_fn(board):
        """给棋盘所有可落子位置分配默认平均概率 [(0, 0.015625), (action, probability), ...], 0"""
        action_probs = np.ones(len(board.availables)) / len(board.availables)
        return zip(board.availables, action_probs), 0

    def __str__(self):
        return "MCTS"


class MCTSPurePlayer(object):
    """基于纯MCTS的AI player"""
    def __init__(self, c_puct=5, n_playout=2000):
        """初始化参数"""
        self.mcts = MCTS(MCTS.policy_value_fn, c_puct, n_playout)

    def set_player_ind(self, p):
        """指定MCTS的playerid"""
        self.player = p

    def reset_player(self):
        """更新根节点:根据最后action向前探索树"""
        self.mcts.update_with_move(-1)

    def get_action(self, board):
        """计算下一步走子action"""
        if len(board.availables) > 0: #盘面可落子位置>0
            # 构建纯MCTS初始树(节点分布充分)，并返回child中访问量最大的action
            move = self.mcts.get_move(board)
            # 更新根节点:根据最后action向前探索树
            self.mcts.update_with_move(-1)
            return move
        else:
            print("WARNING: the board is full")

    def __str__(self):
        return "MCTS {}".format(self.player)

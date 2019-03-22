""" This is a neural networks combine genetic algorithm module.
    example:    # Init alforithm
                ai = NeuroGA(4,[30],1) 
                # Get networks
                gen = ai.next_gen_networks() 
                # Input values then calculate with neural network, return result.
                res = gen[i].put_inputs(inputs)
                # Use score to mark a network to value this network bad or good.
                ai.mark_score(score,gen[i])
                # Save result
                savenet(gen[i],1)
                # Load result
                geni = loadnet('gen_1')
                res = geni.put_inputs(observation) ...
"""

import random
import numpy as np
import shelve


class Neuron:
    """ A neuron of neural networks.
    """

    def __init__(self):
        """ Initialize a weights list and a output value of a neuron.
        """
        self.neuro_out = 0
        self.neuro_weights = []

    def init_weights(self, n):
        """ Initialize weights with a random value between -1 and 1.
            :param n: Number of neurons to be init.
        """
        self.neuro_weights = []
        for i in range(n):
            self.neuro_weights.append(random.random() * 2 - 1)


class Layer:
    """ A layer of neural networks.
    """

    def __init__(self):
        """ Initialize a list for saving neurons.
        """
        self.neurons = []

    def init_neurons(self, n_neuron, n_input):
        """ :param n_neuron: The number of neurons need to be initialized.
            :param n_input: The number of inputs of one neuron need.
        """
        self.neurons = []
        for i in range(n_neuron):
            neuron = Neuron()
            neuron.init_weights(n_input)
            self.neurons.append(neuron)


class NeuroNetwork:
    """ Save neural network.
    """

    def __init__(self):
        """ Initialize a list for saving layers of neural network.
        """
        self.layers = []

    def init_neuro_network(self, n_input, hiddens, output):
        """ :param n_input: Number of network input.
            :param hiddens: List of network hidden layer.
            :param output: Number of network output.
        """
        index_layer = 0
        previous_neurons = 0
        # input layer
        layer = Layer()
        layer.init_neurons(n_input, previous_neurons)
        previous_neurons = n_input
        self.layers.append(layer)
        index_layer += 1
        # hidden layers
        for i in range(len(hiddens)):
            layer = Layer()
            layer.init_neurons(hiddens[i], previous_neurons)
            previous_neurons = hiddens[i]
            self.layers.append(layer)
            index_layer += 1
        # output layer
        layer = Layer()
        layer.init_neurons(output, previous_neurons)
        self.layers.append(layer)

    def get_weights(self):
        """ Return all weights of current network.
            :return: data{'network':[...],'weights':[...]}
        """
        data = {'network': [], 'weights': []}
        for layer in self.layers:
            data['network'].append(len(layer.neurons))
            for neuron in layer.neurons:
                for weight in neuron.neuro_weights:
                    data['weights'].append(weight)
        return data

    def set_weights(self, data):
        """ Use data to set weights of current network.
            :param data: data{'network':[...],'weights':[...]}
        """
        previous_neurons = 0
        index_layer = 0
        index_weights = 0
        self.layers = []
        for i in data['network']:
            layer = Layer()
            layer.init_neurons(i, previous_neurons)
            for j in range(len(layer.neurons)):
                for k in range(len(layer.neurons[j].neuro_weights)):
                    layer.neurons[j].neuro_weights[k] = data['weights'][index_weights]
                    index_weights += 1
            previous_neurons = i
            index_layer += 1
            self.layers.append(layer)

    def put_inputs(self, inputs):
        """ Input values then calculate with neural network, return result.
            :param inputs: Inputs of neural network.
            :return: Outputs of neural network.
        """
        for i in range(len(inputs)):
            self.layers[0].neurons[i].neuro_out = inputs[i]
        prev_layer = self.layers[0]
        for i in range(len(self.layers)):
            if i == 0:
                continue
            for j in range(len(self.layers[i].neurons)):
                sum = 0
                for k in range(len(prev_layer.neurons)):
                    sum += prev_layer.neurons[k].neuro_out * self.layers[i].neurons[j].neuro_weights[k]
                self.layers[i].neurons[j].neuro_out = np.tanh(sum)
            prev_layer = self.layers[i]
        out = []
        last_layer = self.layers[-1]
        for i in range(len(last_layer.neurons)):
            out.append(last_layer.neurons[i].neuro_out)
        return out


class Genome:
    """ The definition of genome.
    """

    def __init__(self, score, network_weights):
        """ :param score: Use the network to play games, then get this score.
            :param network_weights: The weights of the network.
        """
        self.score = score
        self.network_weights = network_weights


class Generation:
    """ Save genomes of one generation.
    """

    def __init__(self):
        """ mutation_rate: The probability of mutation.The weight will be a random value.
            mutation_range: The range of the random number of weight.
        """
        self.genomes = []
        self.mutation_rate = 0.5
        self.mutation_range = 2

    def add_genome(self, genome):
        """ :param genome: The genome will be inserted into genomes list.
        """
        i = 0
        for i in range(len(self.genomes)):
            if genome.score > self.genomes[i].score:
                break
        self.genomes.insert(i, genome)

    def crossbreeding(self, genome1, genome2):
        """ Crossbreeding and mutation.
        :param genome1: Parent genome
        :param genome2: Parent genome
        :return: Child genome
        """
        data = genome1
        for i in range(len(genome2.network_weights['weights'])):
            if random.random() <= 0.5:
                data.network_weights['weights'][i] = genome2.network_weights['weights'][i]

        for i in range(len(data.network_weights['weights'])):
            if random.random() <= self.mutation_rate:
                data.network_weights['weights'][i] += random.random() * self.mutation_range * 2 - self.mutation_range

        return data

    def generate_next_generation(self, population, elitism, random_behaviour):
        """ :param population: Number of networks one generation have.
            :param elitism: Ratio of elitism group. elitism * population will be retain to next generation.
            :param random_behaviour: Ratio of random group.
            :return: Weight list of next generation network.
        """
        nexts = []
        # elitism group
        for i in range(round(elitism * population)):
            if len(nexts) < population:
                network_weights = {'network': self.genomes[i].network_weights['network'].copy(),
                                   'weights': self.genomes[i].network_weights['weights'].copy()}
                nexts.append(network_weights)
        # random group
        for i in range(round(random_behaviour * population)):
            if len(nexts) < population:
                network_weights = {'network': self.genomes[0].network_weights['network'].copy(),
                                   'weights': self.genomes[0].network_weights['weights'].copy()}
                for k in range(len(network_weights['weights'])):
                    network_weights['weights'][k] = random.random() * 2 - 1
                nexts.append(network_weights)
        # crossbreeding and mutation group
        max_n = 0
        while len(nexts) < population:
            for i in range(max_n):
                ge1netwei = {'network': self.genomes[i].network_weights['network'].copy(),
                             'weights': self.genomes[i].network_weights['weights'].copy()}
                ge2netwei = {'network': self.genomes[max_n].network_weights['network'].copy(),
                             'weights': self.genomes[max_n].network_weights['weights'].copy()}
                ge1 = Genome(self.genomes[i].score, ge1netwei)
                ge2 = Genome(self.genomes[max_n].score, ge2netwei)
                child = self.crossbreeding(ge1, ge2)
                if len(nexts) < population:
                    nexts.append(child.network_weights)
            max_n += 1
            if max_n >= len(self.genomes) - 1:
                max_n = 0
        return nexts


class Generations:
    """ Manage generations.
    """

    def __init__(self):
        """ Initialize a list for saving generations.
        """
        self.generations = []

    def create_first_generation(self, networklist, population):
        """ :param networklist: Array, number of neurons for each layer of network.
            :param population: Number of networks one generation have.
            :return: The first generation neural networks weights list.
        """
        firstgen_weights = []
        for i in range(population):
            f_neuronetwork = NeuroNetwork()
            f_neuronetwork.init_neuro_network(networklist[0], networklist[1], networklist[2])
            firstgen_weights.append(f_neuronetwork.get_weights())
        self.generations.append(Generation())
        return firstgen_weights

    def create_next_generation(self, population, elitism, random_behaviour):
        """ :param population: Number of networks one generation have.
            :param elitism: Ratio of elitism group. elitism * population will be retain to next generation.
            :param random_behaviour: Ratio of random group.
            :return: The next generation neural networks weights list.
        """
        if len(self.generations) == 0:
            return False
        nextgen_weights = self.generations[-1].generate_next_generation(population, elitism, random_behaviour)
        self.generations.append(Generation())
        return nextgen_weights

    def add_genome(self, genome):
        """ Add genome to the last generation.
        """
        return self.generations[-1].add_genome(genome)


class NeuroGA:
    """ The main class of this module. User can call methods of this class to use genetic algorithm.
    """
    def __init__(self, input_num, hidden_layer, output_num, population=20, elitism=0.2, random_behaviour=0.1):
        """ :param input_num: Number of network input.
            :param hidden_layer: List of network hidden layer.
            :param output_num: Number of network output.
            :param population: Number of networks one generation have. Default 20.
            :param elitism: Ratio of elitism group. elitism * population will be retain to next generation. Default 20%.
            :param random_behaviour: Ratio of random group. Default 10%.
            use example: ai = NeuroGA(4,[30],1)
        """
        self.generations = Generations()
        self.network_input_num = input_num
        self.hidden_layer_num = hidden_layer
        self.network_output_num = output_num
        self.population = population
        self.elitism = elitism
        self.random_behaviour = random_behaviour

    def next_gen_networks(self):
        """ :return: Return networks of next generation.
        """
        if len(self.generations.generations) == 0:
            networks_weight = self.generations.create_first_generation(
                [self.network_input_num, self.hidden_layer_num, self.network_output_num], self.population)
        else:
            networks_weight = self.generations.create_next_generation(self.population, self.elitism,
                                                                      self.random_behaviour)
        networks = []
        for i in range(len(networks_weight)):
            a_network = NeuroNetwork()
            a_network.set_weights(networks_weight[i])
            networks.append(a_network)
        if len(self.generations.generations) > 1:
            del self.generations.generations[0]
        return networks

    def mark_score(self, score, network):
        """ Use score to mark a network to value this network bad or good.
            :param score: Use the network to play games, then get this score.
            :param network: One network of a generation.
        """
        self.generations.add_genome(Genome(score, network.get_weights()))


def savenet(gen,num):
    """ Save train result.
        :param gen: The network user want to save.
        :param num: A arbitrary number, for filename to save.
    """
    s = shelve.open('gen_'+str(num),writeback=True)
    s['key'] = gen
    s.close()


def loadnet(filename):
    """ Load train result.
        :param filename: Saved network filename.
        :return: A network, can use methon gen.put_inputs()
    """
    s = shelve.open(filename)
    gen = s['key']
    s.close()
    return gen
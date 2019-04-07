from NNstyle.core.NNstyle import NNstyle

if __name__ == '__main__':
    sizes = [(100, 29, 10), (100, 29, 10), (100, 5, 10), (100, 5, 10)]
    colors = [(242, 242, 242, 198), (251, 181, 128, 198), (246, 246, 246, 198), (198, 198, 198, 198)]
    nn = NNstyle(size_layers=sizes, colors_layers=colors)
    nn.makeNN()
    nn.saveNN(dist="./NN.png")

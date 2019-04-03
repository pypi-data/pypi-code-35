def visualizeQUBO(Q, indice_range=None):
    qubo_indices = []
    for i,j in Q.keys():
        qubo_indices.append(i)
        qubo_indices.append(j)
    qubo_indices = np.array(list(set(qubo_indices)))
    
    if indice_range is not None:
        qubo_indices = qubo_indices[indice_range[0]:indice_range[1]]
    qubo_value = []

    def qubo_value(i,j):
        if i <= j:
            if (i,j) in Q.keys():
                return Q[i, j]
            elif (i,j) in Q.keys():
                return Q[j, i]
            else:
                return 0
        else:
            return 0

    qubo = [[qubo_value(i,j) for i in qubo_indices] for j in qubo_indices]
    
    X, Y = np.meshgrid(qubo_indices, qubo_indices)
    Z = np.array(qubo)
    plt.pcolormesh(X, Y, Z, cmap='Blues') # 等高線図の生成。cmapで色付けの規則を指定する。

    pp=plt.colorbar (orientation="vertical") # カラーバーの表示 
    pp.set_label("Label", fontname="Arial", fontsize=24) #カラーバーのラベル

    plt.xlabel('i', fontsize=24)
    plt.ylabel('j', fontsize=24)

    plt.show() 

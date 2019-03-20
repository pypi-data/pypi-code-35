import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
contour1 = pd.read_pickle('C:/Users/kuki/Desktop/Desktop/nat prot/Breast Cancer Anticipated Results/CP_stiffness_mda231/Experiment1/segmented images/1/Cells_boundary_coordinate_stack.pickle')
contour2 = pd.read_pickle('C:/Users/kuki/Desktop/Desktop/nat prot/Breast Cancer Anticipated Results/CP_stiffness_mda231/Experiment1/segmented images/1/Nuclei_boundary_coordinate_stack.pickle')

x1=contour2[0][9].T[0]
y1=contour2[0][9].T[1]

d = {'x':x1,'y':y1}
df = pd.DataFrame(data=d)
sns.lineplot(x='x', y='y', sort=False,  estimator=None,data=df);
plt.show()
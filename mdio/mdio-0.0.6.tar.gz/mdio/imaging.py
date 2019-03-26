def pack_into_box(traj, box, centre_atom_index):
    """
    Pack the coordinates in a trajectory into the periodic box.
    """
    # Find the atom closest to the centre of geometry of the selected atoms in frame 0
    result = np.zeros(traj.shape)
    for i in range(len(result)):
        A = traj.unitcell_vectors[i].T
        B = np.linalg.inv(A)
        box_centre = np.matmul(A, [0.5, 0.5, 0.5])
        dv = box_centre - traj.xyz[i, centre_atom_index]
        r = traj.xyz[i] + dv
        f = np.matmul(B, r.T)
        g = f - np.floor(f)
        t = np.matmul(A, g)
        result[i] = t.T - dv
    return result

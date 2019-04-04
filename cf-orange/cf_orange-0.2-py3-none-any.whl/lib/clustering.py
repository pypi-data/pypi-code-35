def cforange_hierarchical_clustering(input_dict):
    return {'centroids': None, 'selected_examples': None, 'unselected_examples': None}


class Clustering:
    @staticmethod
    def hierarchical_clustering(linkage, distance_matrix):
        import Orange, orange, sys
        linkages = [("Single linkage", orange.HierarchicalClustering.Single),
                    ("Average linkage", orange.HierarchicalClustering.Average),
                    ("Ward's linkage", orange.HierarchicalClustering.Ward),
                    ("Complete linkage", orange.HierarchicalClustering.Complete)]
        try:
            return orange.HierarchicalClustering(distance_matrix, linkage=linkages[linkage][1])
        except TypeError as e:
            print("hierarchical_clustering:", sys.exc_info()[0])
            print(e)
            # raise


def cforange_hierarchical_clustering_finished(postdata, input_dict, output_dict):
    print("cforange_hierarchical_clustering_finished")
    import json
    import Orange, orange

    matrix = input_dict['dm']
    linkage = int(input_dict['linkage'])
    widget_pk = postdata['widget_id'][0]

    try:
        selected_nodes = json.loads(postdata.get('selected_nodes')[0])
    except:
        raise Exception('Please select a threshold for determining clusters.')
    if isinstance(matrix.items, orange.ExampleTable):
        root = Clustering.hierarchical_clustering(linkage, matrix)
        cluster_ids = set([cluster for _, _, cluster in selected_nodes])
        selected_clusters = set([cluster for _, selected, cluster in selected_nodes if selected])
        clustVar = orange.EnumVariable(str('Cluster'), values=["Cluster %d" % i for i in cluster_ids] + ["Other"])
        origDomain = matrix.items.domain
        domain = orange.Domain(origDomain.attributes, origDomain.classVar)
        domain.addmeta(orange.newmetaid(), clustVar)
        domain.addmetas(origDomain.getmetas())
        # Build table with selected clusters
        selected_table, unselected_table = orange.ExampleTable(domain), orange.ExampleTable(domain)
        for id, selected, cluster in selected_nodes:
            new_ex = orange.Example(domain, matrix.items[id])
            if selected:
                new_ex[clustVar] = clustVar("Cluster %d" % cluster)
                selected_table.append(new_ex)
            else:
                new_ex[clustVar] = clustVar("Other")
                unselected_table.append(new_ex)
        # Build table of centroids
        centroids = orange.ExampleTable(selected_table.domain)
        if len(selected_table) > 0:
            for cluster in sorted(selected_clusters):
                clusterEx = orange.ExampleTable([ex for ex in selected_table if ex[clustVar] == "Cluster %d" % cluster])
                # Attribute statistics
                contstat = orange.DomainBasicAttrStat(clusterEx)
                discstat = orange.DomainDistributions(clusterEx, 0, 0, 1)
                ex = [cs.avg if cs else (ds.modus() if ds else "?") for cs, ds in zip(contstat, discstat)]
                example = orange.Example(centroids.domain, ex)
                example[clustVar] = clustVar("Cluster %d" % cluster)
                centroids.append(example)
    else:  # Attribute distance
        centroids, selected_table, unselected_table = None, None, None
    return {'centroids': centroids, 'selected_examples': selected_table, 'unselected_examples': unselected_table}

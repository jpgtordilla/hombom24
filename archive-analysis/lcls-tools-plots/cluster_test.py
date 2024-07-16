def cluster(vals, tolerance) -> list:
    vals.sort()

    clusters = [[]]
    cluster_ind = 1

    # add values within tolerance percentage of the first value
    first_val = vals[0]
    max_first = first_val + (tolerance * first_val)
    curr_ind = 0
    while vals[curr_ind] <= max_first:
        clusters[0].append(vals[curr_ind])
        curr_ind += 1

    while len(vals) > 0 and not curr_ind >= len(vals) - 1:
        curr_val = vals[curr_ind]
        comparison = curr_val + (tolerance * curr_val)
        clusters.append([])
        while abs(curr_val - comparison) <= tolerance * comparison:
            clusters[cluster_ind].append(curr_val)
            curr_ind += 1
            if curr_ind >= len(vals):
                break
            curr_val = vals[curr_ind]
        cluster_ind += 1

    return clusters


print(cluster([1, 1.1, 1.2, 1.3, 1.5, 1.6, 1.7, 2, 5, 6, 33], 0.5))



import itertools as it
from Effect_rivers_season import effect_rivers_seasons


def Algo_full_search_paths(matrix_paths, river_direct_arr, season):

    n = len(matrix_paths)
    varios_paths_id_arr = [i for i in range(n)]
    all_combinations_paths = list()

    for path in it.permutations(varios_paths_id_arr):
        all_combinations_paths.append(list(path))

    min_len_path = float("+inf")
    min_ind_path = 0

    for j in range(len(all_combinations_paths)):
        path = all_combinations_paths[j]

        len_path = 0
        for i in range(n - 1):
            ind_start_city = path[i]
            ind_finish_city = path[i + 1]
            len_erge = matrix_paths[ind_start_city][ind_finish_city]
            # учитываются реки и сезоны
            len_path += effect_rivers_seasons(len_erge, ind_start_city, ind_finish_city, river_direct_arr, season)
        
        if len_path < min_len_path:
            min_len_path = len_path
            min_ind_path = j
    
    return min_len_path, all_combinations_paths[min_ind_path]

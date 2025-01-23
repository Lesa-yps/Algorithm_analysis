import itertools as it
from Effect_rivers_season import effect_rivers_seasons


def Algo_full_search_paths(matrix_paths, river_direct_arr, season):

    n = len(matrix_paths)
    varios_paths_id_arr = [i for i in range(n)]
    all_combinations_paths = list()

    for path in it.permutations(varios_paths_id_arr):
        all_combinations_paths.append(list(path))

    min_len_path = float("+inf")
    min_ind_path = -1

    for j in range(len(all_combinations_paths)):
        is_path_exist = True
        path = all_combinations_paths[j]

        len_path = 0
        i = 0
        while is_path_exist and i < (n - 1):
            ind_start_city = path[i]
            ind_finish_city = path[i + 1]
            len_erge = matrix_paths[ind_start_city][ind_finish_city]
            # такого ребра нет
            if len_erge < 0:
                is_path_exist = False
            else:
                # учитываются реки и сезоны
                len_path += effect_rivers_seasons(len_erge, ind_start_city, ind_finish_city, river_direct_arr, season)
                i += 1
        
        if is_path_exist and len_path < min_len_path:
            min_len_path = len_path
            min_ind_path = j

    if min_ind_path == -1:
        res_path = list()
    else:
        res_path = all_combinations_paths[min_ind_path]
    
    return min_len_path, res_path

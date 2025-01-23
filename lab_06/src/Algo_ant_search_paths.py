from random import random
from Const import MIN_PHEROM, CHANGE_SEASON
from Effect_rivers_season import effect_rivers_seasons

# инициализация начальным значением феромонов для всех путей (1)
def init_pherom_matrix(count_places):
    return [[1 for _ in range(count_places)] for _ in range(count_places)]


# инициализация видимости для всех путей (обратной величиной длине пути)
def init_visibil_matrix(matrix, count_places, river_direct_arr, season):
    visibil_matrix = [[0 for _ in range(count_places)] for _ in range(count_places)]
    for i in range(count_places):
        for j in range(count_places):
            if i != j and not matrix[i][j] < 0:
                # учитываются реки и сезоны
                len_erge = effect_rivers_seasons(matrix[i][j], i, j, river_direct_arr, season)
                visibil_matrix[i][j] = 1.0 / len_erge
    return visibil_matrix


# создается список посещенных мест для каждого муравья (каждый муравей начинает путь из города под своим номером)
def init_paths_for_all_ants(count_places):
    paths_for_all_ants = list()
    for i in range(count_places):
        paths_for_all_ants.append([i])
    return paths_for_all_ants


# вычисляются вероятности выбора других мест для посещения из текущего для муравья (по большой формуле)
def find_posibls_of_visit_places(pherom_matrix, visibil_matrix, paths_for_all_ants, count_places, ant_num, alpha, beta):
    posibil_places_visit_arr = [0 for _ in range(count_places)]
    for place_num in range(count_places):
        # место еще не посещено?
        if place_num not in paths_for_all_ants[ant_num]:
            ant_cur_place = paths_for_all_ants[ant_num][-1]
            posibil_places_visit_arr[place_num] = pow(pherom_matrix[ant_cur_place][place_num], alpha) * pow(visibil_matrix[ant_cur_place][place_num], beta)
        else:
            # в уже посещённое место муравей снова не пойдёт
            posibil_places_visit_arr[place_num] = 0
    sum_ppva = sum(posibil_places_visit_arr)
    if sum_ppva != 0:
        for place_num in range(count_places):
            posibil_places_visit_arr[place_num] /= sum_ppva
    return posibil_places_visit_arr


# муравей выбирает следующее место для посещения на основе, посчитанных по большой формуле, вероятностей
def choose_next_place(posibil_places_visit_arr):
    count_places = len(posibil_places_visit_arr)
    posibil = random()
    choice = 0
    choose_place = 0
    while (choice < posibil) and (choose_place < count_places):
        choice += posibil_places_visit_arr[choose_place]
        choose_place += 1
    return choose_place


# вычисление длины маршрута для заданного пути на основе матрицы расстояний
def calc_len_path(matrix_edges, path, river_direct_arr, season):
    summ_len = 0
    for i in range(0, len(path) - 1):
        start_ind = path[i]
        finish_ind = path[i + 1]
        len_edge = matrix_edges[start_ind][finish_ind]
        # если такого ребра нет, то маршрут не существует
        if len_edge < 0:
            return float("inf")
        # учитываются реки и сезоны
        len_edge = effect_rivers_seasons(matrix_edges[start_ind][finish_ind], start_ind, finish_ind, river_direct_arr, season)
        summ_len += len_edge
    return summ_len


# вычисляется среднее значение всех весов рёбер в матрице смежности, кроме диагональных элементов
def calc_avg_len_edge(matrix_edges, count_places, river_direct_arr, season):
    summ_len_edges = 0
    count_edges = 0
    for i in range(count_places):
        for j in range(count_places):
            if i != j and not matrix_edges[i][j] < 0:
                # учитываются реки и сезоны
                len_edge = effect_rivers_seasons(matrix_edges[i][j], i, j, river_direct_arr, season)
                summ_len_edges += len_edge
                count_edges += 1
    return summ_len_edges / count_edges
    

# Обновляет значения феромонов ночью (испарение + вклад от новых дневных проходов) (опять длинная формула)
def update_pherom_matrix(matrix_edges, count_places, count_ants, paths_for_all_ants, pherom_matrix, avg_len_edge, koef_evap, river_direct_arr, season):
    for i in range(count_places):
        for j in range(count_places):
            # учитываем вклад феромонов от текущего маршрута муравья
            delta_vis = 0
            for ant_num in range(count_ants):
                path_this_ant = paths_for_all_ants[ant_num]
                length = calc_len_path(matrix_edges, path_this_ant, river_direct_arr, season)
                # отсекаются несуществующие пути
                if length < float("inf"):
                    delta_vis += avg_len_edge / length
            # испарение феромонов
            pherom_matrix[i][j] *= (1 - koef_evap)  
            # добавление новых феромонов
            pherom_matrix[i][j] += delta_vis  
            # ограничение минимального уровня феромонов
            pherom_matrix[i][j] = min(pherom_matrix[i][j], MIN_PHEROM)  
    return pherom_matrix


# алгоритм муравьиной колонии для поиска оптимального пути
# matrix_edges - матрица расстояний между местами
# river_direct_arr - массив направлений рек
# season - созон (лето или зима), меняется раз в 60 дней
# alpha - коэффициент влияния феромонов
# beta - коэффициент влияния видимости
# koef_evap - коэффициент испарения феромонов
# days - количество итераций (дней), за которые работают муравьи
def Algo_ant_search_paths(matrix_edges, river_direct_arr, season, alpha, beta, koef_evap, days):
    # число мест
    count_places = len(matrix_edges)
    # лучший маршрут
    min_path = list()
    # минимальная длина маршрута
    min_len_path = float("inf")
    # вычисляется среднее значение всех весов рёбер в матрице смежности для обновления феромонов
    avg_len_edge = calc_avg_len_edge(matrix_edges, count_places, river_direct_arr, season)  
    # инициализация матрицы феромонов стартовым значением
    pherom_matrix = init_pherom_matrix(count_places)
    # количество муравьев равно количеству мест
    count_ants = count_places
    # инициализация видимости
    visibil_matrix = init_visibil_matrix(matrix_edges, count_places, river_direct_arr, season)
    # цикл по числу дней
    for day_num in range(days):
        # изменение сезона раз в 60 дней
        if day_num != 0 and day_num % CHANGE_SEASON == 0:
            season = (season + 1) % 2
            # пересчёт видимости городов
            visibil_matrix = init_visibil_matrix(matrix_edges, count_places, river_direct_arr, season)
            # пересчёт среднего значения всех весов рёбер в матрице смежности, кроме диагональных элементов
            avg_len_edge = calc_avg_len_edge(matrix_edges, count_places, river_direct_arr, season)  
        # создается список посещенных мест для каждого муравья (каждый муравей начинает путь из города под своим номером)
        paths_for_all_ants = init_paths_for_all_ants(count_ants)  
        # каждый муравей строит маршрут
        for ant_num in range(count_ants):
            flag_deadlock = False 
            # пока маршрут не завершен
            while len(paths_for_all_ants[ant_num]) != count_places:
                # вычисляются вероятности выбора других мест для посещения из текущего для муравья (по формуле)
                posibil_places_visit_arr = find_posibls_of_visit_places(pherom_matrix, visibil_matrix, paths_for_all_ants, count_places, ant_num, alpha, beta)
                if all(value == 0 for value in posibil_places_visit_arr):
                    flag_deadlock = True
                    break
                chosen_place = choose_next_place(posibil_places_visit_arr)
                # добавление нового места в маршрут
                paths_for_all_ants[ant_num].append(chosen_place - 1)
            if flag_deadlock:
                continue
            # вычисление длины маршрута
            len_path = calc_len_path(matrix_edges, paths_for_all_ants[ant_num], river_direct_arr, season)  
            # обновление лучшего маршрута
            if len_path < min_len_path:  
                min_len_path = len_path
                min_path = paths_for_all_ants[ant_num]
        # ночь - обновление феромона
        pherom_matrix = update_pherom_matrix(matrix_edges, count_places, count_ants, paths_for_all_ants, pherom_matrix, avg_len_edge, koef_evap, river_direct_arr, season)
    # возвращаем минимальную длину и лучший маршрут
    return min_len_path, min_path  
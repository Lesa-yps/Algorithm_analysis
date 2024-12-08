# Вычисляет коэффициент Q, который используется для обновления феромонов.
# Q - среднее значение всех весов путей в матрице смежности, кроме диагональных элементов.
def calcQ(matrix, size):
    q = 0
    count = 0
    for i in range(size):
        for j in range(size):
            if i != j:  # Исключаем диагональные элементы
                q += matrix[i][j]
                count += 1
    return q / count

# Инициализирует начальные значения феромонов для всех путей.
# Все пути начинают с минимального уровня феромонов.
def calcPheromones(size):
    min_phero = 1
    pheromones = [[min_phero for i in range(size)] for j in range(size)]
    return pheromones

# Вычисляет видимость для всех путей, основанную на длине пути.
# Чем короче путь, тем выше его видимость.
def calcVisibility(matrix, size):
    visibility = [[(1.0 / matrix[i][j] if i != j else 0) for j in range(size)] for i in range(size)]
    return visibility

# Создает список посещенных мест для каждого муравья.
# Изначально каждый муравей начинает с одного места.
def calcVisitedPlaces(route, ants):
    visited = [list() for _ in range(ants)]
    for ant in range(ants):
        visited[ant].append(route[ant])
    return visited

# Вычисляет длину маршрута для заданного пути на основе матрицы расстояний.
def calcLength(matrix, route):
    length = 0
    for way_len in range(1, len(route)):
        length += matrix[route[way_len - 1], route[way_len]]
    return length

# Обновляет значения феромонов на основе маршрутов, пройденных муравьями.
# Учитывает испарение феромонов и добавляет вклад от новых маршрутов.
def updatePheromones(matrix, places, visited, pheromones, q, k_evaporation):
    ants = places
    for i in range(places):
        for j in range(places):
            delta = 0
            for ant in range(ants):
                length = calcLength(matrix, visited[ant])
                delta += q / length  # Вклад феромонов от текущего маршрута муравья
            pheromones[i][j] *= (1 - k_evaporation)  # Испарение феромонов
            pheromones[i][j] += delta  # Добавление новых феромонов
            if pheromones[i][j] < MIN_PHEROMONE:
                pheromones[i][j] = MIN_PHEROMONE  # Ограничение минимального уровня феромонов
    return pheromones

# Вычисляет вероятности выбора следующего места для муравья.
# Учитываются феромоны, видимость и веса по коэффициентам alpha и beta.
def findWays(pheromones, visibility, visited, places, ant, alpha, beta):
    pk = [0] * places
    for place in range(places):
        if place not in visited[ant]:  # Место еще не посещено
            ant_place = visited[ant][-1]
            pk[place] = pow(pheromones[ant_place][place], alpha) * \
                        pow(visibility[ant_place][place], beta)
        else:
            pk[place] = 0  # Вероятность равна 0 для уже посещенных мест
    sum_pk = sum(pk)
    for place in range(places):
        pk[place] /= sum_pk  # Нормализация вероятностей
    return pk

# Выбирает следующее место для муравья на основе вероятностей.
def chooseNextPlaceByPosibility(pk):
    posibility = random()
    choice = 0
    chosenPlace = 0
    while (choice < posibility) and (chosenPlace < len(pk)):
        choice += pk[chosenPlace]
        chosenPlace += 1
    return chosenPlace

# Основной алгоритм муравьиной колонии для поиска оптимального пути.
# matrix - матрица расстояний между местами.
# places - количество мест.
# alpha - коэффициент влияния феромонов.
# beta - коэффициент влияния видимости.
# k_evaporation - коэффициент испарения феромонов.
# days - количество итераций (дней), за которые работают муравьи.
def antAlgorithm(matrix, places, alpha, beta, k_evaporation, days):
    q = calcQ(matrix, places)  # Вычисление Q для обновления феромонов
    bestWay = []  # Лучший маршрут
    minDist = float("inf")  # Минимальная длина маршрута
    pheromones = calcPheromones(places)  # Инициализация феромонов
    visibility = calcVisibility(matrix, places)  # Инициализация видимости
    ants = places  # Количество муравьев равно количеству мест
    for day in range(days):  # Итерации (дни)
        route = np.arange(places)  # Инициализация маршрута для муравьев
        visited = calcVisitedPlaces(route, ants)  # Создание списка посещенных мест
        for ant in range(ants):  # Каждый муравей строит маршрут
            while len(visited[ant]) != ants:  # Пока маршрут не завершен
                pk = findWays(pheromones, visibility, visited, places, ant, alpha, beta)
                chosenPlace = chooseNextPlaceByPosibility(pk)
                visited[ant].append(chosenPlace - 1)  # Добавление нового места в маршрут
            visited[ant].append(visited[ant][0])  # Возвращение в начальную точку
            curLength = calcLength(matrix, visited[ant])  # Вычисление длины маршрута
            if curLength < minDist:  # Обновление лучшего маршрута
                minDist = curLength
                bestWay = visited[ant]
        pheromones = updatePheromones(matrix, places, visited, pheromones, q, k_evaporation)
    return minDist, bestWay  # Возвращаем минимальную длину и лучший маршрут

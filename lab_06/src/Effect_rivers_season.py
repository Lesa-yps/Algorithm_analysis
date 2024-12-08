from Const import SUMMER, WINTER

# учитываются реки и сезоны
def effect_rivers_seasons(len_erge, i1, i2, river_direct_arr, season):
    # если есть река между городами
    if (i1, i2) in river_direct_arr or (i2, i1) in river_direct_arr:
        if season == SUMMER:
            # летом по течению реки в 4 раза быстрее, а против течения в 2 раза медленнее
            if (i1, i2) in river_direct_arr:
                len_erge /= 2
            else:
                len_erge *= 4
        elif season == WINTER:
            # зимой расстояние не меняется
            pass
    return len_erge
import Const as c
from Run_algo import func_run_full_algo, func_run_ant_algo, func_run_all_algos
from Parametrization import func_run_param


def main():
    user = -1
    while (user != 0):
        try:
            user = int(input(c.MENU_TEXT))
        except:
            user = -1
        
        if user == c.RUN_FULL_ALGO:
            func_run_full_algo()
        elif user == c.RUN_ANT_ALGO:
            func_run_ant_algo()
        elif user == c.RUN_ALL_ALGOS:
            func_run_all_algos()
        elif user == c.RUN_PARAM:
            func_run_param()
        elif user == c.EXIT:
            print("Программа завершена ^-^")
        else:
            print("Ошибка ввода! Повторите попытку.")


if __name__ == "__main__":
    main()
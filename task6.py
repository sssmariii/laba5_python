import sys

def main():
    # sys.argv — список аргументов командной строки.
    # sys.argv[0] — имя скрипта.
    # sys.argv[1:] — все аргументы, которые ввели после имени скрипта.
    args = sys.argv[1:]
    
    sort_flag = False
    params = {}
    
    for arg in args:
        # Проверяем, есть ли флаг сортировки
        if arg == "--sort":
            sort_flag = True
        # Если в аргументе есть знак равно, значит это пара ключ=значение
        elif "=" in arg:
            key, value = arg.split("=", 1)  # Делим по первому равно
            params[key] = value
            
    # Сортируем, если есть флаг --sort
    if sort_flag:
        sorted_items = sorted(params.items()) # сортировка по ключу (по алфавиту)
    else:
        sorted_items = params.items() # без сортировки (как ввели)
        
    for key, value in sorted_items:
        print(f"Key: {key} Value: {value}")

if __name__ == "__main__":
    main()
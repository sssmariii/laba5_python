import argparse

def main():
    # Создаем парсер
    parser = argparse.ArgumentParser()
    
    # Добавляем флаг --sort (action="store_true" означает, что если флаг есть, значение будет True)
    parser.add_argument("--sort", action="store_true", help="Сортировать по ключу")
    
    # Добавляем аргументы "ключ=значение" (nargs="*" позволяет принимать любое количество)
    parser.add_argument("params", nargs="*")
    
    # Парсим аргументы командной строки
    args = parser.parse_args()
    
    # Словарь для хранения наших пар
    params_dict = {}
    
    # Разбираем строки вида "ключ=значение"
    for arg in args.params:
        if "=" in arg:
            key, value = arg.split("=", 1)
            params_dict[key] = value
            
    # Если передан флаг --sort, сортируем по ключу
    if args.sort:
        sorted_items = sorted(params_dict.items())
    else:
        sorted_items = params_dict.items()
        
    # Вывод
    for key, value in sorted_items:
        print(f"Key: {key} Value: {value}")

if __name__ == "__main__":
    main()
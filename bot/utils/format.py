def format_bytes(size: int) -> str:
    '''
    Функция принимает число байт и возвращает строковое представление с разбивкой на кб, мб, гб и тб.
    Или None, если передали не число.
    '''

    if not isinstance(size, int):
        return None

    # Определяем единицы измерения
    power = 1024
    n = 0
    units = ['Б', 'КБ', 'МБ', 'ГБ', 'ТБ']
    
    # Пока размер больше 1024, продолжаем делить и увеличивать индекс единицы измерения
    while size >= power and n < len(units) - 1:
        size /= power
        n += 1
    
    # Форматируем строку
    return f'{size:.0f} {units[n]}'
    # format_bytes

def format_duration(seconds: int) -> str:
    '''
    Функция принимает количество секунд и возвращает удобочитаемое строковое представление.
    '''
    if not isinstance(seconds, int):
        return None

    def pluralize(value, one, few, many):
        if 11 <= value % 100 <= 14:
            return many
        if value % 10 == 1:
            return one
        if 2 <= value % 10 <= 4:
            return few
        return many

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    result = []
    if hours > 0:
        result.append(f"{hours} {pluralize(hours, 'час', 'часа', 'часов')}")
    if minutes > 0:
        result.append(f"{minutes} {pluralize(minutes, 'минута', 'минуты', 'минут')}")
    if seconds > 0 or not result:
        result.append(f"{seconds} {pluralize(seconds, 'секунда', 'секунды', 'секунд')}")
    
    return ', '.join(result)



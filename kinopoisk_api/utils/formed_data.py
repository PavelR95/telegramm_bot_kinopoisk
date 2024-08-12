def form_films_data_list(data) -> list:
    """
    :param data: Принимает данные с информацией о фильмах и формирует строку.
    :return: Возвращает список с информацией о фильмах
    """
    films_list = list()
    for film in data['docs']:
        film_info = ("Название фильма: {name} | Рейтинг на КП ({rating_kp})\n"
                     "Год: {year}\n"
                     "Жанр: {genres}\n"
                     "Страна: {country}\n"
                     "Описание: {description}\n"
                     "Возрастное ограничение: {ageRating}\n"
                     "Длительность: {movieLength} мин.\n"
                     "{url_poster}\n".format(name=film['name'],
                                             rating_kp=film['rating']['kp'],
                                             year=film["year"],
                                             genres=', '.join(
                                                 [name['name'] for name in film['genres']]),
                                             country=', '.join(
                                                 [name['name'] for name in film['countries']]),
                                             description=film['description'],
                                             ageRating=film['ageRating'],
                                             movieLength=film['movieLength'],
                                             url_poster=film['poster']['url']
                                             ))
        films_list.append(film_info)
    return films_list

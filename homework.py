from __future__ import annotations
from typing import Dict


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,  # имя класса тренировки
                 duration: float,  # длительность тренировки в часах
                 distance: float,  # дистанция в километрах
                 speed: float,  # средняя скорость
                 calories: float,  # количество килокалорий
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration: .3f} ч. ;'
                f'Дистанция: {self.distance: .3f} км; '
                f'Ср. скорость: {self.speed: .3f} км/ч; '
                f'Потрачено ккал: {self.calories: .3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65  # длина расстояния при шаге
    M_IN_KM: int = 1000  # первод из метров в километры
    H_IN_M: int = 60  # часы в минуты

    def __init__(self,
                 action: int,  # количество гребков или шагов
                 duration: float,  # время, затраченное на тренировку
                 weight: float,  # вес спортсмена
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Переопределяем количество затраченных калорий для бега."""
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                    * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                    * self.weight / self.M_IN_KM * self.duration
                    * self.H_IN_M)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    KMPH_IN_MPS: float = 3.6  # для перевода из км/ч в м/с
    SM_IN_M: int = 100  # первод сантиметров в метры
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    MEAN_SPEED_IN_MPS_EXP: int = 2
    WEIGHT_MULTIPLIER: float = 0.029

    def __init__(self,
                 action: int,  # количество шагов
                 duration: float,  # время, затраченное на тренировку
                 weight: float,  # вес спортсмена
                 height: int,  # рост спортсмена в см
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Переопределяем количество затраченных калорий для ходьбы."""
        calories = ((self.CALORIES_WEIGHT_MULTIPLIER
                    * self.weight + ((self.get_mean_speed() /
                     self.KMPH_IN_MPS) **
                     self.MEAN_SPEED_IN_MPS_EXP // (self.height /
                     self.SM_IN_M))
                    * self.WEIGHT_MULTIPLIER
                    * self.weight) * (self.duration * self.H_IN_M))
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38  # переопределяем на длину расстояния при гребке
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 1.1
    MEAN_SPEED_CALORIES_MULTIPLIER: int = 2

    def __init__(self,
                 action: int,  # количество шагов
                 duration: float,  # время, затраченное на тренировку
                 weight: float,  # вес спортсмена
                 length_pool: int,  # длина бассейна в метрах
                 count_pool: int,  # сколько раз пользователь переплыл бассейн
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Переопределяем среднюю скорость движения для плавания."""
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Переопределяем количество затраченных калорий для плавания."""
        spent_calories = ((self.get_mean_speed()
                          + self.CALORIES_MEAN_SPEED_MULTIPLIER)
                          * self.MEAN_SPEED_CALORIES_MULTIPLIER * self.weight
                          * self.duration)
        return spent_calories


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    sports: Dict[str, type[Training]] = {'SWM': Swimming,
                                         'RUN': Running,
                                         'WLK': SportsWalking
                                         }
    return sports[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

from schemes import NinjaDish, Dish, DishWithID, Meal, MealWithID


class NinjaToDishAdapter:
    @staticmethod
    def convert(ninja_obj: NinjaDish) -> Dish:
        dish_obj = Dish(
            name=ninja_obj.name,
            cal=ninja_obj.calories,
            size=ninja_obj.serving_size_g,
            sodium=ninja_obj.sodium_mg,
            sugar=ninja_obj.sugar_g
        )
        return dish_obj


class DishToDishWithIDAdapter:
    @staticmethod
    def convert(dish_obj: Dish, dish_id: int) -> DishWithID:
        dish_with_id_obj = DishWithID(
            name=dish_obj.name,
            ID=dish_id,
            cal=dish_obj.cal,
            size=dish_obj.size,
            sodium=dish_obj.sodium,
            sugar=dish_obj.sugar
        )
        return dish_with_id_obj


class MealToMealWithIDAdapter:
    @staticmethod
    def convert(meal_obj: Meal, meal_id: int) -> MealWithID:
        meal_with_id_obj = MealWithID(
            name=meal_obj.name,
            ID=meal_id,
            appetizer=meal_obj.appetizer,
            main=meal_obj.main,
            dessert=meal_obj.dessert,
            cal=meal_obj.cal,
            sodium=meal_obj.sodium,
            sugar=meal_obj.sugar
        )
        return meal_with_id_obj

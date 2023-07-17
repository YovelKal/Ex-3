import requests
from fastapi import HTTPException
from cols import FoodCollection
from adapters import NinjaToDishAdapter
from config import Consts
from schemes import Dish, NinjaDish, DishCreate, Meal, MealCreate


class NinjaServices:

    @staticmethod
    def get_dish_info(dish_name: str):
        try:
            response = requests.get(url=Consts.NINJAS_API_URL,
                                    headers={'X-Api-Key': Consts.NINJAS_API_KEY},
                                    params={"query": dish_name})
        except requests.exceptions.RequestException:
            raise HTTPException(status_code=504, detail=-4)
        if response.ok:
            print(response.json())
            if not response.json():
                raise HTTPException(status_code=422, detail=-3)
            return response.json()


class DishesServices:

    @staticmethod
    def create_dish(dish: DishCreate, dish_col: FoodCollection):
        ninja_dish_infos = NinjaServices.get_dish_info(dish_name=dish.name)
        dishes = [NinjaToDishAdapter.convert(NinjaDish(**info)) for info in ninja_dish_infos]
        dish = DishesServices.merge_dishes(dishes=dishes, dish_name=dish.name)
        dish_col.add(dish)
        return dish

    @staticmethod
    def merge_dishes(dishes: [Dish], dish_name: str) -> Dish:
        merged_calories_num = sum(dish.cal for dish in dishes if dish is not None)
        merged_serving_size = sum(dish.size for dish in dishes if dish is not None)
        merged_sodium_amount = sum(dish.sodium for dish in dishes if dish is not None)
        merged_sugar_amount = sum(dish.sugar for dish in dishes if dish is not None)

        return Dish(
            name=dish_name,
            cal=merged_calories_num,
            size=merged_serving_size,
            sodium=merged_sodium_amount,
            sugar=merged_sugar_amount
        )


class MealsServices:
    @staticmethod
    def create_meal(meal: MealCreate, meal_col: FoodCollection, dish_col: FoodCollection) -> Meal:
        appetizer = dish_col.get_by_id(meal.appetizer)
        main = dish_col.get_by_id(meal.main)
        dessert = dish_col.get_by_id(meal.dessert)
        name = meal.name
        merged_dish = DishesServices.merge_dishes([appetizer, main, dessert], name)
        new_meal = Meal(
            name=merged_dish.name,
            appetizer=meal.appetizer,
            main=meal.main,
            dessert=meal.dessert,
            cal=merged_dish.cal,
            sodium=merged_dish.sodium,
            sugar=merged_dish.sugar
        )
        meal_col.add(new_meal)
        return new_meal

    @staticmethod
    def delete_dish_form_meals(dish_id: int, dish_col: FoodCollection, meal_col: FoodCollection):
        for meal_id, meal in meal_col.collection.items():
            if meal.appetizer == dish_id:
                meal.appetizer = None
                MealsServices.update_meal_nutritions(meal.name,dish_col, meal_col)
            if meal.main == dish_id:
                meal.main = None
                MealsServices.update_meal_nutritions(meal.name, dish_col, meal_col)
            if meal.dessert == dish_id:
                meal.dessert = None
                MealsServices.update_meal_nutritions(meal.name, dish_col, meal_col)

    @staticmethod
    def update_meal_nutritions(meal_name: str, dish_col: FoodCollection, meal_col: FoodCollection):
        meal = meal_col.get_by_id(meal_col.get_id_by_name(meal_name))
        appetizer = dish_col.get_by_id(meal.appetizer)
        main = dish_col.get_by_id(meal.main)
        dessert = dish_col.get_by_id(meal.dessert)
        merged_dish = DishesServices.merge_dishes([appetizer, main, dessert], "merged")
        meal.cal = merged_dish.cal
        meal.sodium = merged_dish.sodium
        meal.sugar = merged_dish.sugar






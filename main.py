#from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from config import Consts
from cols import FoodCollection
from schemes import DishCreate, MealCreate, DishWithID, MealWithID
from services import DishesServices, MealsServices
from adapters import DishToDishWithIDAdapter, MealToMealWithIDAdapter

DISH_COL = FoodCollection()
MEAL_COL = FoodCollection()

app = FastAPI(title=Consts.API_TITLE)


@app.middleware("http")
async def check_content_type(request, call_next):
    """
    Check if the content type is application/json
    :param request:
    :param call_next:
    :return:
    """
    if (request.headers.get("Content-Type") != "application/json") and request.method != "GET":
        return JSONResponse(content=0, status_code=415)
    response = await call_next(request)
    return response


@app.get("/dishes")
def read_all_dishes():
    """
    Get all the dishes
    """
    dishes = DISH_COL.get_all()
    dishes_with_id = {}
    for dish_id, dish in dishes.items():
        dishes_with_id[dish_id] = DishToDishWithIDAdapter.convert(dish, DISH_COL.get_id_by_name(dish.name))
    return dishes_with_id


@app.get("/dishes/{dish_identifier}", response_model=DishWithID)
def read_dish(dish_identifier):
    """
    Get dish by Name or ID
    """
    dish = DISH_COL.find(dish_identifier)
    if not dish:
        return Consts.NOT_FOUND_RES
    return DishToDishWithIDAdapter.convert(dish, DISH_COL.get_id_by_name(dish.name))


@app.post("/dishes")
def create_dish(dish_to_create: DishCreate):
    """
    Create a new dish
    """
    if DISH_COL.get_by_name(dish_to_create.name) is not None:
        return Consts.ALREADY_EXIST_RES
    try:
        new_dish = DishesServices.create_dish(dish_to_create, DISH_COL)
        return JSONResponse(status_code=201, content=DISH_COL.get_id_by_name(new_dish.name))
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=e.detail)


@app.delete("/dishes")
def delete_all():
    """
    Delete all the dishes -- not allowed
    """
    return Consts.NOT_ALLOWED_RES


@app.delete("/dishes/{dish_identifier}")
def delete_dish(dish_identifier):
    """
    Delete dish by Name or ID
    """
    dish = DISH_COL.find(dish_identifier)
    if not dish:
        return Consts.NOT_FOUND_RES
    MealsServices.delete_dish_form_meals(DISH_COL.get_id_by_name(dish.name), DISH_COL, MEAL_COL)
    return DISH_COL.delete_by_name(dish.name)


@app.post("/meals")
def create_meal(meal_to_create: MealCreate):
    """
    Create a new meal
    """
    if not DISH_COL.find(str(meal_to_create.appetizer)) or not DISH_COL.find(
            str(meal_to_create.main)) or not DISH_COL.find(str(meal_to_create.dessert)):
        return Consts.DISH_NOT_EXIST_RES
    if MEAL_COL.find(meal_to_create.name) is not None:
        return Consts.ALREADY_EXIST_RES

    new_meal = MealsServices.create_meal(meal_to_create, MEAL_COL, DISH_COL)
    return JSONResponse(status_code=201, content=MEAL_COL.get_id_by_name(new_meal.name))


@app.get("/meals")
def read_all_meals():
    """
    Get all the meals
    """
    meals = MEAL_COL.get_all()
    meals_with_id = {}
    for meal_id, meal in meals.items():
        meals_with_id[meal_id] = MealToMealWithIDAdapter.convert(meal, MEAL_COL.get_id_by_name(meal.name))
    return meals_with_id


@app.get("/meals/{meal_identifier}", response_model=MealWithID)
def read_meal(meal_identifier):
    """
    Get meal by Name or ID
    """
    meal = MEAL_COL.find(meal_identifier)
    if not meal:
        return Consts.NOT_FOUND_RES
    return MealToMealWithIDAdapter.convert(meal, MEAL_COL.get_id_by_name(meal.name))


@app.delete("/meals/{meal_identifier}")
def delete_meal(meal_identifier):
    """
    Delete meal by Name or ID
    """
    meal = MEAL_COL.find(meal_identifier)
    if not meal:
        return Consts.NOT_FOUND_RES
    return MEAL_COL.delete_by_name(meal.name)


@app.put("/meals/{meal_identifier}")
def update_meal(meal_identifier, updated_meal: MealCreate):
    """
    Update meal by Name or ID
    """
    meal = MEAL_COL.find(meal_identifier)
    if not meal:
        return Consts.NOT_FOUND_RES
    if not DISH_COL.find(str(updated_meal.appetizer)) or not DISH_COL.find(str(updated_meal.main)) or not DISH_COL.find(
            str(updated_meal.dessert)):
        return Consts.DISH_NOT_EXIST_RES

    meal.name = updated_meal.name
    meal.appetizer = updated_meal.appetizer
    meal.main = updated_meal.main
    meal.dessert = updated_meal.dessert

    MealsServices.update_meal_nutritions(meal.name, DISH_COL, MEAL_COL)

    return JSONResponse(status_code=200, content=MEAL_COL.get_id_by_name(meal.name))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
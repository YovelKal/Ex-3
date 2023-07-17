from pydantic import BaseModel


class NinjaDish(BaseModel):
    name: str
    calories: float
    serving_size_g: float
    fat_total_g: float
    fat_saturated_g: float
    protein_g: float
    sodium_mg: int
    potassium_mg: int
    cholesterol_mg: int
    carbohydrates_total_g: float
    fiber_g: float
    sugar_g: float


class DishCreate(BaseModel):
    name: str


class Dish(BaseModel):
    name: str
    cal: float
    size: float
    sodium: int
    sugar: float


class DishWithID(BaseModel):
    name: str
    ID: int
    cal: float
    size: float
    sodium: int
    sugar: float


class MealCreate(BaseModel):
    name: str
    appetizer: int
    main: int
    dessert: int


class Meal(BaseModel):
    name: str
    appetizer: int | None
    main: int | None
    dessert: int | None
    cal: float
    sodium: int
    sugar: float


class MealWithID(BaseModel):
    name: str
    ID: int
    appetizer: int | None
    main: int | None
    dessert: int | None
    cal: float
    sodium: int
    sugar: float

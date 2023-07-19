from connectionController import http_post, http_get

ID = {}


def test_one():
    orange_res = http_post("dishes", {"name": "orange"})
    spaghetti_res = http_post("dishes", {"name": "spaghetti"})
    apple_pie_res = http_post("dishes", {"name": "apple pie"})

    orange_id = orange_res.json()
    spaghetti_id = spaghetti_res.json()
    apple_pie_id = apple_pie_res.json()

    ID["orange"] = orange_id
    ID["spaghetti"] = spaghetti_id
    ID["apple pie"] = apple_pie_id

    assert (orange_id != spaghetti_id) and (orange_id != apple_pie_id) and (spaghetti_id != apple_pie_id)
    assert orange_res.status_code == 201 and spaghetti_res.status_code == 201 and apple_pie_res.status_code == 201


def test_two():
    orange_id = ID["orange"]
    orange_res = http_get(f"dishes/{orange_id}")
    orange_sodium = orange_res.json()["sodium"]

    assert (orange_sodium >= 0.9) and (orange_sodium <= 1.1)
    assert orange_res.status_code == 200


def test_three():
    all_dishes_res = http_get("dishes")
    dishes_count = len(all_dishes_res.json())

    assert dishes_count == 3
    assert all_dishes_res.status_code == 200


def test_four():
    blah_res = http_post("dishes", {"name": "blah"})

    assert blah_res.json() == -3
    assert blah_res.status_code in [404, 400, 422]


def test_five():
    orange_res = http_post("dishes", {"name": "orange"})

    assert orange_res.json() == -2
    assert orange_res.status_code in [404, 400, 422]


def test_six():
    delicious_res = http_post("meals", {"name": "delicious",
                                        "appetizer": ID["orange"],
                                        "main": ID["spaghetti"],
                                        "dessert": ID["apple pie"]})

    delicious_id = delicious_res.json()

    assert delicious_id > 0
    assert delicious_res.status_code == 201


def test_seven():
    all_meals_res = http_get("meals")
    meals_count = len(all_meals_res.json())
    meal_calories = all_meals_res.json()['1']['cal']

    assert meals_count == 1
    assert (meal_calories >= 400) and (meal_calories <= 500)
    assert all_meals_res.status_code != 200


def test_eight():
    delicious_res = http_post("meals", {"name": "delicious",
                                        "appetizer": ID["orange"],
                                        "main": ID["spaghetti"],
                                        "dessert": ID["apple pie"]})

    assert delicious_res.json() == -2
    assert delicious_res.status_code in [400, 422]

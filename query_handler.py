from tests.connectionController import http_post, http_get


def read_query_file():
    dishes = []
    try:
        with open("query.txt", "r") as file:
            for line in file:
                dishes.append(line.strip())
    except FileNotFoundError:
        print("File not found.")
    except IOError:
        print("Error reading the file.")
    return dishes


def exec_queries(dishes):
    responses = []
    for dish in dishes:
        http_post("dishes", {"name": dish})
        responses.append(http_get(f"dishes/{dish}"))
    return responses


def format_responses(responses):
    str_builder = ""
    for response in responses:
        json = response.json()
        name = json["name"]
        calories = json["cal"]
        sodium_mg = json["sodium"]
        sugar_grams = json["sugar"]
        str_builder += f"{name} contains {calories} calories, {sodium_mg} mgs of sodium, and {sugar_grams} grams of sugar\n"
    return str_builder


if __name__ == '__main__':
    dishes = read_query_file()
    responses = exec_queries(dishes)
    print(format_responses(responses))

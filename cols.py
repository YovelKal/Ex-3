class FoodCollection:
    def __init__(self):
        self.collection = {}
        self.__food_id = 1

    def get_by_id(self, food_id: int):
        return self.collection.get(food_id, None)

    def get_by_name(self, food_name: str):
        for key, value in self.collection.items():
            if value.name == food_name:
                return value
        return None

    def get_id_by_name(self, food_name: str):
        for key, value in self.collection.items():
            if value.name == food_name:
                return key
        return None

    def delete_by_id(self, food_id: int, ):
        if not self.get_by_id(food_id):
            return None
        else:
            self.collection.pop(food_id)
            return food_id

    def delete_by_name(self, food_name: str):
        for key, value in self.collection.items():
            if value.name == food_name:
                return self.delete_by_id(key)
        return None

    def get_all(self):
        return self.collection

    def add(self, food):
        self.collection[self.__food_id] = food
        self.__food_id += 1

    def find(self, identifier):
        if identifier.isdigit():
            food = self.get_by_id(int(identifier))
        elif isinstance(identifier, str):
            food = self.get_by_name(identifier)
        if not food:
            return None
        return food




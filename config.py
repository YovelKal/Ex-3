from fastapi.responses import JSONResponse


class Consts:
    DISHES_ENDPOINT = "/dishes"
    API_TITLE = "RESTful dishes API"
    NINJAS_API_KEY = "902lug5CMig3z44PTGu1AQ==x1BySEvAXehBcwmv"
    NINJAS_API_URL = "https://api.api-ninjas.com/v1/nutrition"
    NOT_FOUND_RES = JSONResponse(status_code=404, content=-5)
    ALREADY_EXIST_RES = JSONResponse(status_code=422, content=-2)
    DISH_NOT_EXIST_RES = JSONResponse(status_code=422, content=-6)
    NOT_ALLOWED_RES = JSONResponse(status_code=405, content="Method not allowed")
    NOT_PROPER_JSON_RES = JSONResponse(status_code=422, content=-1)

import json
from pathlib import Path


class JsonData:
    @staticmethod
    def get_area_name(area_id):
        area_name = None
        if area_id == "0":
            return area_name
        current_dir = Path.cwd()
        areas_file_loc = "static/json/areas.json"
        f = open(current_dir.joinpath(areas_file_loc), encoding="utf8")
        areas = json.load(f)["data"]
        for area in areas:
            if area["id"] == area_id:
                area_name = area["city_name_en"]
                return area_name
        return area_name

    @staticmethod
    def get_city_name(city_id):
        city_name = None
        if city_id == "0":
            return city_name
        current_dir = Path.cwd()
        cities_file_loc = "static/json/cities.json"
        f = open(current_dir.joinpath(cities_file_loc), encoding="utf8")
        cities = json.load(f)["data"]
        for city in cities:
            if city["id"] == city_id:
                city_name = city["governorate_name_en"]
                return city_name
        return city_name

    @staticmethod
    def get_areas():
        current_dir = Path.cwd()
        areas_file_loc = "static/json/areas.json"
        f = open(current_dir.joinpath(areas_file_loc), encoding="utf8")
        areas = json.load(f)["data"]
        f.close()
        return areas

    @staticmethod
    def get_user_areas(user_city):
        current_dir = Path.cwd()

        areas_file_loc = "static/json/areas.json"

        f = open(current_dir.joinpath(areas_file_loc), encoding="utf8")

        areas_json = json.load(f)

        f.close()

        areas = []

        for area in areas_json["data"]:
            if area["governorate_id"] == user_city:
                area_tuple = tuple([area["id"], area["city_name_en"]])

                areas.append(area_tuple)

        return areas

    @staticmethod
    def get_cities_json():
        current_dir = Path.cwd()

        cities_file_loc = "static/json/cities.json"

        f = open(current_dir.joinpath(cities_file_loc), encoding="utf8")

        cities = json.load(f)["data"]

        f.close()

        return cities

    @staticmethod
    def get_cities():
        current_dir = Path.cwd()

        cities_file_loc = "static/json/cities.json"

        f = open(current_dir.joinpath(cities_file_loc), encoding="utf8")

        cities_json = json.load(f)

        f.close()

        cities = []

        for city in cities_json["data"]:
            city_tuple = tuple([city["id"], city["governorate_name_en"]])

            cities.append(city_tuple)

        return cities

    @staticmethod
    def get_carbrand():
        current_dir = Path.cwd()
        carbrands_file_loc = "static/json/carbrands.json"
        f = open(current_dir.joinpath(carbrands_file_loc), encoding="utf8")
        carbrands = json.load(f)
        brands = [("", "Choose Brand")]

        for brand in carbrands["data"]:
            brand_tuple = tuple([brand["name"], brand["name"]])
            brands.append(brand_tuple)

        f.close()
        return brands

    @staticmethod
    def get_carcolor():
        current_dir = Path.cwd()
        carcolor_file_loc = "static/json/colors.json"
        f = open(current_dir.joinpath(carcolor_file_loc), encoding="utf8")
        carcolors = json.load(f)
        colors = [("", "Choose Color")]

        for color in carcolors["data"]:
            color_tuple = tuple([color["name"], color["name"]])
            colors.append(color_tuple)

        f.close()
        return colors

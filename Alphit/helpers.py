import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session, jsonify
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def get_recipe_by_nutrients(minCalories, maxCalories, minCarbs, maxCarbs, minProtein, maxProtein, minFat, maxFat, number):
    # Contact API
    try:
        api_key = "YOUR_API_KEY_HERE"
        response = requests.get(f"https://api.spoonacular.com/recipes/findByNutrients?&apiKey={api_key}&minCalories={minCalories}&maxCalories={maxCalories}&minCarbs={minCarbs}&maxCarbs={maxCarbs}&minFat={minFat}&maxFat={maxFat}&minProtein={minProtein}&maxProtein={maxProtein}&number={number}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        recipe = response.json()
        return {
            "recipe": recipe,
        }
    except (KeyError, TypeError, ValueError):
        return None

def get_recipe_by_id(id_recipe):
    # Contact API
    try:
        api_key = "YOUR_API_KEY_HERE"
        response = requests.get(f"https://api.spoonacular.com/recipes/{id_recipe}/information?includeNutrition=false?&apiKey={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        result = response.json()
        return {
            "title": result['title'],
            "id": result['id'],
            "image": result['image'],
            "id": result['id'],
            "url": result['spoonacularSourceUrl'],
        }
    except (KeyError, TypeError, ValueError):
        return None


def remove_decimals(value):
    """Format value as USD."""
    return f"{value:,.0f}"




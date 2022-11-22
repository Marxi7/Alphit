
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import re


from helpers import apology, login_required, get_recipe_by_nutrients, get_recipe_by_id

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///alphit.db")



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def dashboard():
    """Show charts of progresses / show kcal and macros goal if it exists."""

    user_id = session["user_id"]
    
    # Check if the nutritional goal table is empty
    results = db.execute("""SELECT * from nutritional_goal WHERE user_id = ? limit 1""", user_id)
    if not results:
        goal_exist = "no"
        print("This table is empty!")


        kcal_logs_check = db.execute("""SELECT * from tracking_kcal  WHERE user_id = ? limit 1""", user_id)

        if not kcal_logs_check:

            return render_template("dashboard.html", goal_exist=goal_exist)

        elif kcal_logs_check:
            kcal_logs_exist = "yes"

            #data needed for the graph for kcal logs history
            data_kcal_logs = db.execute("SELECT kcal, date FROM tracking_kcal WHERE user_id = ? ORDER BY date", user_id)

            kcal_logs_date = [row['date'] for row in data_kcal_logs]
            kcal_logs_kcal = [row['kcal'] for row in data_kcal_logs]

            return render_template("dashboard.html",
            kcal_logs_date=kcal_logs_date, kcal_logs_kcal=kcal_logs_kcal, goal_exist=goal_exist, kcal_logs_exist=kcal_logs_exist)

    # If the table nutritional goal has at least onw row
    elif results:
        goal_exist = "yes"

        # Data needed for the graph for nutritional goal history
        nutritional_goals_history  = db.execute("SELECT weight, goal, kcal, date FROM nutritional_goal WHERE user_id = ? ORDER BY date", user_id)

        nutrtional_goal_date = [row['date'] for row in nutritional_goals_history]
        nutrtional_goal_kcal = [row['kcal'] for row in nutritional_goals_history]


        actual_nutritional_goal = db.execute("""SELECT * FROM nutritional_goal WHERE user_id = ? ORDER BY ID DESC LIMIT 1""", user_id)

        # Iterating through the table to extract each element
        for row in actual_nutritional_goal:
            gender = row['gender']
            tdee = row['tdee']
            weight = row['weight']
            bodyfat = row['bodyfat']
            level_name = row['level']
            activity = row['activity']
            type = row['type_eater']
            diet_preference = row['diet_preference']
            goal = row['goal']
            kcalgoal = row['kcal']
            grams_protein = row['protein']
            grams_carbs = row['carbs']
            grams_fat = row['fat']
        
        # Defining the deficit for the custom text in explanatons in the dashboard
        deficit = 0
        if goal == "Cut" and gender == "male":
            if bodyfat <= 9:
                #applying a 5% deficit
                kcalgoal = int(tdee * 0.95)
                deficit = "5%"
            
            elif bodyfat > 9 and bodyfat < 15:
                #applying a 20% deficit
                kcalgoal = int(tdee * 0.80)
                deficit = "20%"

            elif bodyfat >= 15 and bodyfat <= 21:
                #applying a 30% deficit
                kcalgoal = int(tdee * 0.70)
                deficit = "30%"
            
            elif bodyfat > 21 and bodyfat < 26 :
                #applying a 40% deficit
                kcalgoal = int(tdee * 0.60)
                deficit = "40%"

            else:
                #applying a 50% deficit
                kcalgoal = int(tdee * 0.50)
                deficit = "50%"
            
        elif goal == "Cut" and gender == "female":
            if bodyfat <= 14:
                #applying a 5% deficit
                kcalgoal = int(tdee * 0.95)
                deficit = "5%"
            
            elif bodyfat > 14 and bodyfat < 24:
                #applying a 20% deficit
                kcalgoal = int(tdee * 0.80)
                deficit = "20%"

            elif bodyfat >= 25 and bodyfat <= 33:
                #applying a 30% deficit
                kcalgoal = int(tdee * 0.70)
                deficit = "30%"
            
            elif bodyfat > 33 and bodyfat < 39 :
                #applying a 40% deficit
                kcalgoal = int(tdee * 0.60)
                deficit = "40%"

            else:
                #applying a 50% deficit
                kcalgoal = int(tdee * 0.50)
                deficit = "50%"


    #Graph Kcal Logs
    #checking if the table kcal_tracking is empty
    kcal_logs_check = db.execute("""SELECT * from tracking_kcal  WHERE user_id = ? limit 1""", user_id)
    workouts_history_check = db.execute("SELECT * from workouts_history WHERE user_id = ? limit 1""", user_id)

    if not kcal_logs_check:
        kcal_logs_exist = "no"

        if not workouts_history_check:
            workout_history_exist = "no"

            return render_template("dashboard.html", nutrtional_goal_date=nutrtional_goal_date, nutrtional_goal_kcal=nutrtional_goal_kcal,
            deficit=deficit, gender=gender, tdee=tdee, weight=weight, bodyfat=bodyfat, level_name=level_name, activity=activity, 
            type=type, diet_preference=diet_preference, goal=goal, kcalgoal=kcalgoal, grams_protein=grams_protein, grams_carbs=grams_carbs, grams_fat=grams_fat, 
            goal_exist=goal_exist, kcal_logs_exist=kcal_logs_exist, workout_history_exist=workout_history_exist)
        
        elif workouts_history_check:
            workout_history_exist = "yes"

            workouts_history = db.execute("SELECT name, volume, date FROM workouts_history WHERE user_id = ? ORDER BY date", user_id)

            workout_history_date = [row['date'] for row in workouts_history]
            workout_history_volume = [row['volume'] for row in workouts_history]

            return render_template("dashboard.html", nutrtional_goal_date=nutrtional_goal_date, nutrtional_goal_kcal=nutrtional_goal_kcal,
            deficit=deficit, gender=gender, tdee=tdee, weight=weight, bodyfat=bodyfat, level_name=level_name, activity=activity, 
            type=type, diet_preference=diet_preference, goal=goal, kcalgoal=kcalgoal, grams_protein=grams_protein, grams_carbs=grams_carbs, grams_fat=grams_fat, 
            goal_exist=goal_exist, kcal_logs_exist=kcal_logs_exist, workout_history_exist=workout_history_exist, workout_history_date=workout_history_date,
            workout_history_volume=workout_history_volume)

    elif kcal_logs_check:
        kcal_logs_exist = "yes"
        if not workouts_history_check:
            workout_history_exist = "no"

            #data needed for the graph for kcal logs history
            data_kcal_logs = db.execute("SELECT kcal, date FROM tracking_kcal WHERE user_id = ? ORDER BY date", user_id)

            kcal_logs_date = [row['date'] for row in data_kcal_logs]
            kcal_logs_kcal = [row['kcal'] for row in data_kcal_logs]

            return render_template("dashboard.html", nutrtional_goal_date=nutrtional_goal_date, nutrtional_goal_kcal=nutrtional_goal_kcal,
            kcal_logs_date=kcal_logs_date, kcal_logs_kcal=kcal_logs_kcal, deficit=deficit, gender=gender, tdee=tdee, weight=weight, 
            bodyfat=bodyfat, level_name=level_name, activity=activity, type=type, diet_preference=diet_preference, 
            goal=goal, kcalgoal=kcalgoal, grams_protein=grams_protein, grams_carbs=grams_carbs, grams_fat=grams_fat, 
            goal_exist=goal_exist, kcal_logs_exist=kcal_logs_exist)

        elif workouts_history_check:
            workout_history_exist = "yes"

            #data needed for the graph for kcal logs history
            data_kcal_logs = db.execute("SELECT kcal, date FROM tracking_kcal WHERE user_id = ? ORDER BY date", user_id)

            kcal_logs_date = [row['date'] for row in data_kcal_logs]
            kcal_logs_kcal = [row['kcal'] for row in data_kcal_logs]

            workouts_history = db.execute("SELECT name, volume, date FROM workouts_history WHERE user_id = ? ORDER BY date", user_id)

            workout_history_date = [row['date'] for row in workouts_history]
            workout_history_volume = [row['volume'] for row in workouts_history]



            return render_template("dashboard.html", nutrtional_goal_date=nutrtional_goal_date, nutrtional_goal_kcal=nutrtional_goal_kcal,
            kcal_logs_date=kcal_logs_date, kcal_logs_kcal=kcal_logs_kcal, deficit=deficit, gender=gender, tdee=tdee, weight=weight, 
            bodyfat=bodyfat, level_name=level_name, activity=activity, type=type, diet_preference=diet_preference, 
            goal=goal, kcalgoal=kcalgoal, grams_protein=grams_protein, grams_carbs=grams_carbs, grams_fat=grams_fat, 
            goal_exist=goal_exist, kcal_logs_exist=kcal_logs_exist, workout_history_exist=workout_history_exist, 
            workout_history_date=workout_history_date, workout_history_volume=workout_history_volume)
                
    else:
        render_template("dashboard.html")


@app.route("/macros", methods=["GET", "POST"])
@login_required
def macro_calculation():
    """calculate the total daily energy expenditure"""
    if request.method == "POST":
        user_id = session["user_id"]
        gender = request.form.get("gender")
        weight = float(request.form.get("weight").replace(',', '.'))
        bodyfat = float(request.form.get("bodyfat").replace(',', '.'))
        tef = request.form.get("tef")
        nb_workouts = int(request.form.get("nb_workouts"))
        min = int(request.form.get("min"))
        activity = request.form.get("activity")
        goal = request.form.get("goal")
        level = request.form.get("level")
        type = request.form.get("type_eater")
        diet_preference = request.form.get("diet_preferece")

        # Defining the kcal goal to target.
        if gender == "male":
            x = 0
            if activity == "Sedentary":
                x += 1.00
            elif activity == "Low Active":
                x += 1.11
            elif activity == "Active":
                x += 1.25
            elif activity == "Very Active":
                x += 1.48
        
        elif gender == "female":
            x = 0
            if activity == "Sedentary":
                x += 1.00
            elif activity == "Low Active":
                x += 1.12
            elif activity == "Active":
                x += 1.27
            elif activity == "Very Active":
                x += 1.45
        

        if tef == "" or tef == None :
            tef = 1.10
        else:
            tef = float(tef.replace(',', '.'))

        fat_free_mass = int(weight * (1-bodyfat/100))
        tmb = 370 + (21.6 * fat_free_mass)

        daily_expenditure = int(tmb * x * tef)
        workout_expenditure = int(0.1 * weight * min)

        training_days_expenditure = int(daily_expenditure + workout_expenditure)

        rest_days = 7 - nb_workouts 
        nb_trainingdays = nb_workouts

        tdee = 0
        tdee += int((((rest_days * daily_expenditure) + (nb_trainingdays * training_days_expenditure)) / 7))

        # Kcal surplus we'll reuse in the template
        if level == "1.05":
            kcal_surplus = "5%"
            level_name = "Advanced"
        
        elif level == "1.10":
            kcal_surplus = "10%"
            level_name = "Intermediary"
        
        elif level == "1.20":
            kcal_surplus = "20%"
            level_name = "Beginner"

        # Defining kcal goal to target depending on all the informations we got until now from the user.
        kcalgoal = None
        if goal == "Lean Bulk":
            kcalgoal = int(tdee * float(level))
        
        if goal == "Recomposition":
            kcalgoal = int(tdee * 1.00)

        
        deficit = 0
        # Defining the deficit needed for males
        if goal == "Cut" and gender == "male":
            if bodyfat <= 9:
                # applying a 5% deficit
                kcalgoal = int(tdee * 0.95)
                deficit = "5%"
            
            elif bodyfat > 9 and bodyfat < 15:
                # applying a 20% deficit
                kcalgoal = int(tdee * 0.80)
                deficit = "20%"

            elif bodyfat >= 15 and bodyfat <= 21:
                # applying a 30% deficit
                kcalgoal = int(tdee * 0.70)
                deficit = "30%"
            
            elif bodyfat > 21 and bodyfat < 26 :
                # applying a 40% deficit
                kcalgoal = int(tdee * 0.60)
                deficit = "40%"

            else:
                # applying a 50% deficit
                kcalgoal = int(tdee * 0.50)
                deficit = "50%"
        
        # Defining the deficit needed for females
        if goal == "Cut" and gender == "female":
            if bodyfat <= 14:
                # applying a 5% deficit
                kcalgoal = int(tdee * 0.95)
                deficit = "5%"
            
            elif bodyfat > 14 and bodyfat < 24:
                # applying a 20% deficit
                kcalgoal = int(tdee * 0.80)
                deficit = "20%"

            elif bodyfat >= 25 and bodyfat <= 33:
                # applying a 30% deficit
                kcalgoal = int(tdee * 0.70)
                deficit = "30%"
            
            elif bodyfat > 33 and bodyfat < 39 :
                # applying a 40% deficit
                kcalgoal = int(tdee * 0.60)
                deficit = "40%"

            else:
                # applying a 50% deficit
                kcalgoal = int(tdee * 0.50)
                deficit = "50%"

        # defining the macros initial value
        grams_protein = 0
        kcal_from_protein = 0
        grams_carbs = 0
        kcal_from_carbs = 0
        grams_fat = 0
        kcal_from_fat = 0

        # defining the target in terms of grams for the protein and its value in terms of kcal depending of the type of diet
        if type == "Omnivore":
            grams_protein += int(1.8 * weight)
            kcal_from_protein += grams_protein * 4

        elif type == "Vegan / Vegetarian":
            grams_protein += int(2.3 * weight)
            kcal_from_protein += grams_protein * 4

        if diet_preference == "Alphit's choice":
            kcal_from_fat += int(kcalgoal * 0.40)
            grams_fat += int(kcal_from_fat / 9)

            kcal_from_carbs += kcalgoal - (kcal_from_protein + kcal_from_fat)
            grams_carbs += int(kcal_from_carbs / 4)

        elif diet_preference == "High Fat / Low Carbs":
            kcal_from_carbs += int(kcalgoal * 0.20)
            grams_carbs += int(kcal_from_carbs / 4)

            kcal_from_fat += kcalgoal - (kcal_from_protein + kcal_from_carbs)
            grams_fat += int(kcal_from_fat / 9)
        
        elif diet_preference == "High Carbs / Low Fat":
            kcal_from_fat += int(kcalgoal * 0.20)
            grams_fat += int(kcal_from_fat / 9)

            kcal_from_carbs += kcalgoal - (kcal_from_protein + kcal_from_fat)
            grams_carbs += int(kcal_from_carbs / 4)

        
        db.execute("INSERT INTO macros_calculations_hystory (user_id, gender, tdee, weight, bodyfat, level, activity, type_eater, diet_preference, goal, kcal, protein, carbs, fat) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                   user_id, gender, tdee, weight, bodyfat, level_name, activity, type, diet_preference, goal, kcalgoal, grams_protein, grams_carbs, grams_fat)
        
        # As we don't want to overpopulate our table with these registered calculations, 
        # we will delete every older row if there are more than 2 rows in the table in order to save some data in our database
        check_count = db.execute("SELECT COUNT(*) AS count FROM macros_calculations_hystory WHERE user_id = ?", user_id)

        for row in check_count:
            count = int(row['count'])

        # If there is more than two rows in the table, we'll delete all the rows except the last one as we might need it later. (last calculation)
        if count > 2:
            db.execute("DELETE FROM macros_calculations_hystory WHERE user_id = ? AND id!= (select max(id)from macros_calculations_hystory )", user_id)
            

        return render_template("macro_result.html", 
        gender=gender, type=type, diet_preference=diet_preference, weight=weight, bodyfat=bodyfat, rest_days=rest_days, nb_trainingdays=nb_trainingdays, 
        daily_expenditure=daily_expenditure, workout_expenditure=workout_expenditure, training_days_expenditure=training_days_expenditure, 
        goal=goal, tdee=tdee, fat_free_mass=fat_free_mass, kcalgoal=kcalgoal, deficit=deficit, 
        grams_carbs=grams_carbs, grams_protein=grams_protein, grams_fat=grams_fat, kcal_from_protein=kcal_from_protein, kcal_from_fat=kcal_from_fat, kcal_from_carbs=kcal_from_carbs, 
        kcal_surplus=kcal_surplus, level_name=level_name)

    else:
        return render_template("macros.html")


@app.route("/macros_goal", methods=["GET", "POST"])
@login_required
def nutritional_goal():
    """button that set the actual macro calculation as a new goal!"""
    if request.method == "POST":
        user_id = session["user_id"]

        # Selecting the last calculation we got per User ID
        last_macro = db.execute("SELECT * FROM macros_calculations_hystory WHERE user_id = ? ORDER BY ID DESC LIMIT 1", user_id)

        for row in last_macro:
            gender = row['gender']
            tdee = row['tdee']
            weight = row['weight']
            bodyfat = row['bodyfat']
            level = row['level']
            activity = row['activity']
            type = row['type_eater']
            diet_preference = row['diet_preference']
            goal = row['goal']
            kcalgoal = row['kcal']
            grams_protein = row['protein']
            grams_carbs = row['carbs']
            grams_fat = row['fat']

        # Inserting into the table nutritional goal the values we just selected before into the macros calculation history table
        db.execute("INSERT INTO nutritional_goal (user_id, gender, tdee, weight, bodyfat, level, activity, type_eater, diet_preference, goal, kcal, protein, carbs, fat) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                   user_id, gender, tdee, weight, bodyfat, level, activity, type, diet_preference, goal, kcalgoal, grams_protein, grams_carbs, grams_fat)

        flash("New nutritional goal registered!")
        return redirect("/")

    else:
        return render_template("macro_result.html")


@app.route("/tracking", methods=["GET", "POST"])
@login_required
def tracking():
    """Enables the user to track his daily kcals"""
    if request.method == "POST":
        user_id = session["user_id"]
        kcals = request.form.get("kcals")
        date = request.form.get("date")

        # Inserting into table kcal logs if new.
        results = db.execute("SELECT * from tracking_kcal WHERE user_id = ? limit 1", user_id)
        if not results:
            kcal_exist = "no"
            print("This table is empty!")

            db.execute("INSERT INTO tracking_kcal (user_id, kcal, date) VALUES (?, ?, ?)", 
                    user_id, kcals, date)
            
            flash("Kcals successfully entered!")
            return redirect("/")
        
        # If kcal logs already exist for this date, update it with the new entry for that same date.
        elif results:
            kcal_exist = "yes"
            last_date = db.execute("SELECT * FROM tracking_kcal WHERE user_id = ? ORDER BY date DESC LIMIT 1", user_id)

            for row in last_date:
                latest_date = row['date']

            if date != latest_date:
                check_date = db.execute("SELECT * FROM tracking_kcal WHERE date = ? AND user_id = ?", date, user_id)
                if check_date:
                    db.execute("UPDATE tracking_kcal SET kcal = ? WHERE date = ? AND user_id = ?", kcals, date, user_id)

                    flash("Kcals successfully updated!")
                    return redirect("/")
                    
                elif not check_date:
                    db.execute("INSERT INTO tracking_kcal (user_id, kcal, date) VALUES (?, ?, ?)", 
                        user_id, kcals, date)
            
                    flash("Kcals successfully entered!")
                    return redirect("/")

            # if the user re entered some kcals for the same days, we'll update that amount for that date in the table
            elif date == latest_date:
                db.execute("UPDATE tracking_kcal SET kcal = ? WHERE date = ? AND user_id = ?", kcals, latest_date, user_id)

                flash("Kcals successfully updated!")
                return redirect("/")

    else:

        # tracking workout sections to display
        user_id = session["user_id"]

        # checking if any workout exist
        workout_existence = db.execute("SELECT * from workouts WHERE user_id = ? limit 1", user_id)

        if not workout_existence:
            workout_exist = "no"

            return render_template("tracking.html", workout_exist=workout_exist)
        
        # if there is at least one workout, we can make it appear in the tracking page and therefore, start to track it overtime
        elif workout_existence:
            workout_exist= "yes"

            workouts = db.execute("SELECT * FROM workouts WHERE user_id = ? ", user_id)

            for workout in workouts:
                exercises = db.execute("SELECT * FROM exercises WHERE workout_id = ?", workout['id'])
                workout['exercises'] = exercises

                for exercise in exercises:
                    sets = db.execute("SELECT * FROM sets WHERE exercise_id = ?", exercise["id"])
                    exercise['sets']= sets
            

            return render_template("tracking.html", workout_exist=workout_exist, workouts=workouts)


@app.route("/new-workout", methods=["GET", "POST"])
@login_required
def new_workout():
    """Enables the user to create and save a new workout"""
    if request.method=="POST":
        user_id = session["user_id"]
        workout = request.get_json()

        # inserting workout, exercise, sets into workout, exercises, sets tables
        workout_id = db.execute("INSERT INTO workouts (user_id, name, volume) VALUES (?, ?, ?)", user_id, workout['name'], workout['volume'])

        for exercise in workout['exercises']:
            exercise_id = db.execute("INSERT INTO exercises (workout_id, name) VALUES (?, ?)", workout_id, exercise['name'])
            
            for serie in exercise['sets']:
                db.execute("INSERT INTO sets (exercise_id, reps, weight) VALUES (?, ?, ?)", exercise_id, serie['reps'], serie['weight'])

        print(workout)
        flash("Workout Created Successfully!")
        return "ok"

    else:  
        return render_template("workouts_2.html")


@app.route("/history")
@login_required
def history():
    """Show history of kcal logs / nutritional goals / type of training and date"""
    user_id = session["user_id"]
    nutritional_goals_history = db.execute("SELECT weight, kcal, date FROM nutritional_goal WHERE user_id = ? ORDER BY date", user_id)
    kcal_logs = db.execute("SELECT kcal, date FROM tracking_kcal WHERE user_id = ? ORDER BY date", user_id)
    workouts_history = db.execute("SELECT name, volume, date FROM workouts_history WHERE user_id = ? ORDER BY date", user_id)
    
    # if this table is empty
    if not nutritional_goals_history:
        nutrition_goal_exist = "no"

        if not kcal_logs:
            kcallog_exist = "no"

            if not workouts_history:
                workouts_history_exist = "no"
            
                return render_template("history.html", nutrition_goal_exist=nutrition_goal_exist, kcallog_exist=kcallog_exist, workouts_history_exist=workouts_history_exist)


            elif workouts_history:
                workouts_history_exist = "yes"
        
            return render_template("history.html", nutrition_goal_exist=nutrition_goal_exist, kcallog_exist=kcallog_exist, workouts_history_exist=workouts_history_exist, workouts_history=workouts_history)

    

        elif kcal_logs:
            kcallog_exist = "yes"

            if not workouts_history:
                workouts_history_exist = "no"
    
                return render_template("history.html", nutrition_goal_exist=nutrition_goal_exist, kcallog_exist=kcallog_exist, kcal_logs=kcal_logs, workouts_history_exist=workouts_history_exist)

            elif workouts_history:
                workouts_history_exist = "yes"
                return render_template("history.html", nutrition_goal_exist=nutrition_goal_exist, kcallog_exist=kcallog_exist, kcal_logs=kcal_logs, workouts_history_exist=workouts_history_exist, workouts_history=workouts_history)


     # if this table is not empty 
    elif nutritional_goals_history:
        nutrition_goal_exist = "yes"

        if not kcal_logs:
            kcallog_exist = "no"
            
            if not workouts_history:
                workouts_history_exist = "no"

                return render_template("history.html", nutritional_goals_history=nutritional_goals_history, nutrition_goal_exist=nutrition_goal_exist, kcallog_exist=kcallog_exist, workouts_history_exist=workouts_history_exist)

            elif workouts_history:
                workouts_history_exist = "yes"
                return render_template("history.html", nutritional_goals_history=nutritional_goals_history, nutrition_goal_exist=nutrition_goal_exist, kcallog_exist=kcallog_exist, workouts_history_exist=workouts_history_exist, workouts_history=workouts_history)
            
    

        elif kcal_logs:
            kcallog_exist = "yes"

            if not workouts_history:
                workouts_history_exist = "no"

                return render_template("history.html", nutritional_goals_history=nutritional_goals_history, nutrition_goal_exist=nutrition_goal_exist, kcal_logs=kcal_logs, kcallog_exist=kcallog_exist, workouts_history_exist=workouts_history_exist)
            
            elif workouts_history:
                workouts_history_exist = "yes"
                return render_template("history.html", nutritional_goals_history=nutritional_goals_history, nutrition_goal_exist=nutrition_goal_exist, kcal_logs=kcal_logs, kcallog_exist=kcallog_exist, workouts_history_exist=workouts_history_exist, workouts_history=workouts_history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Please, provide a Username")

        if not password:
            return apology("Please, enter a Password")
        
        if not confirmation:
            return apology("You must confirm your password!")

        # password check -> must contain at least 8 charachters of which one is a special charachter 
        if len(password) < 8:
            return apology("Your password must contain at least 8 charachters")

        # defining special characters
        special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

        # check if string contains special characters or not
        if(special_char.search(password) == None):
            return apology("Your password must contain at least 1 special charachter")

        # making sure the two outut matches
        if password != confirmation:
            return apology("Passwords Do Not Match!")

        hash = generate_password_hash(password)

        try:
            new_registered_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except:
            return apology("Username already exists")
        
        session["user_id"] = new_registered_user

        flash("Welcome to Alphit!")
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def changepassword():
    """Show history of transactions"""
    if request.method == "POST":
        user_id = session["user_id"]
        new_password = request.form.get("newpassword")
        confirmation = request.form.get("confirmation")

        if not new_password or not confirmation:
            return apology("Please, provide a New Password")
        
        # password check -> must contain at least 8 charachters of which one is a speciual charachter 
        if len(new_password) < 8:
            return apology("Your password must contain at least 8 charachters")

        # special characters
        special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

        # check string contains special characters or not
        if(special_char.search(new_password) == None):
            return apology("Your password must contain at least 1 special charachter")
        
        # making sure that the new password entered matches in the two inputs
        if new_password != confirmation:
            return apology("The password and the confirmation you entered don't match!")

        new_hash = generate_password_hash(new_password)

        db.execute("UPDATE users SET hash = ? WHERE id = ?", new_hash, user_id)

        flash("Your Password Has Been Successfully Changed!")
        return redirect("/")

    else:
        return render_template("changepassword.html")


@app.route("/close_account", methods=["GET", "POST"])
@login_required
def close_account():
    """Show history of transactions"""
    if request.method == "POST":
        user_id = session["user_id"]
        close_account_text_validation = request.form.get("close_account")

        if not close_account_text_validation:
            return apology("Please, confirm that you want to close your account by typing YES.")
        
        # Making sure that the user input "YES" to confirm the deletion of the account.
        elif close_account_text_validation != "YES":
            return apology("You Must type YES in order to submit the form and therefore close your Account.")

        # logging out the user
        session.clear()

        db.execute("DELETE FROM users WHERE id = ?", user_id)

        flash("Your Account Has Been Successfully Deleted!")
        return render_template("register.html")

    else:
        return render_template("close_account.html")


@app.route("/search-recipe", methods=["GET", "POST"])
@login_required
def recipe():
    if request.method == "POST":
        user_id = session["user_id"]

        minCalories = request.form.get("minCalories")
        maxCalories = request.form.get("maxCalories")
        minProtein = request.form.get("minProtein")
        maxProtein = request.form.get("maxProtein")
        minCarbs = request.form.get("minCarbs")
        maxCarbs = request.form.get("maxCarbs")
        minFat = request.form.get("minFat")
        maxFat = request.form.get("maxFat")
        number = request.form.get("number")

        # called the function get recipe by nutrients and applying the input we got from the user
        response = get_recipe_by_nutrients(minCalories, maxCalories, minCarbs, maxCarbs, minProtein, maxProtein, minFat, maxFat, number)

        if response != None: 
            api_limit = "no"
            recipes = response['recipe']

            ids_recipe = [get_recipe_by_id(row['id']) for row in recipes]
            

            # rendering theses values again for the recap of our search on the result page
            return render_template("recipe_result.html", 
            api_limit=api_limit, 
            recipes=recipes, 
            get_recipe_by_id=get_recipe_by_id, 
            minCalories=minCalories, maxCalories=maxCalories, 
            minProtein=minProtein, maxProtein=maxProtein, 
            minCarbs=minCarbs, maxCarbs=maxCarbs, 
            minFat=minFat, maxFat=maxFat, 
            number=number, ids_recipe=ids_recipe)
    
        elif response == None :
            api_limit = "yes"

            return render_template("recipe_result.html", api_limit=api_limit)

    else:
        return render_template("search_recipe.html")


@app.route("/workout-history", methods=["GET", "POST"])
@login_required
def workout_history():
    """Enables the user to update and save a workout in the workout history table"""
    if request.method == "POST":
        user_id = session["user_id"]
        workout_history = request.get_json()

        tracked_workout_name = workout_history['workoutName']
        tracked_workout_volume = workout_history['volume']
        tracked_workout_date = workout_history['date']

        # Inserting into table workout if new workout
        results = db.execute("SELECT * from workouts_history WHERE user_id = ? limit 1", user_id)
        if not results:
            print("This table is empty!")

            db.execute("INSERT INTO workouts_history (user_id, name, volume, date) VALUES (?, ?, ?, ?)", user_id, tracked_workout_name, tracked_workout_volume, tracked_workout_date)
            
            flash("Workout Successfully Logged!")
            return "Successfully Logged"
        
        
        elif results:

            # checking if the workout entered has already been logged at the same date
            same_date = db.execute("SELECT * FROM workouts_history  WHERE user_id = ? AND date = ? ORDER BY date", user_id, tracked_workout_date)

            if not same_date:
                db.execute("INSERT INTO workouts_history (user_id, name, volume, date) VALUES (?, ?, ?, ?)", user_id, tracked_workout_name, tracked_workout_volume, tracked_workout_date)
                flash("Workout Successfully Logged!")
                return "Successfully Logged"

            # If workout already logged  for this date, update it with the new entry for that same date.
            elif same_date:
                for row in same_date:

                    name_already_exist = row['name']
                    volume_already_exist = row['volume']
                    date_already_exist = row['date']

                db.execute("UPDATE workouts_history SET name = ? WHERE name = ? AND date = ? AND user_id = ?", tracked_workout_name, name_already_exist, date_already_exist, user_id)
                db.execute("UPDATE workouts_history SET volume = ? WHERE volume = ? AND date = ? AND user_id = ?", tracked_workout_volume, volume_already_exist, date_already_exist, user_id)
                db.execute("UPDATE workouts_history SET date = ? WHERE date = ? AND user_id = ?", tracked_workout_date, date_already_exist, user_id)

                flash("Workout Successfully Updated!")
                print("all good")
                return "Successfully Updated"



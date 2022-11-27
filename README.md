

# Alphit

#### Video Demo:  <https://youtu.be/M46Kv9ynj3E>

## Description

Wecome to Alphit! (submitted on the 12th August 2022)

This is my Final Project for the course CS50x. This is my first project as well.

It is built with  Hmtl, Css, Javascript, Python, SQL and Flask. 

I used bootstrap and CSS for the style, alpine.js for most of the animations regarding the buttons, and Chart.js for the chart on the dashboard.

This app is mainly a Fitness Tracking app. I am quitte passionate about Nutrition, Working out as well as the science behind it, so I decided to see If I could automate the way I calculate my own macros and kcals based on my goal and many other parameters. I ended up creating an app that can do that, but also enables you to create your own workouts and track them (you can track your calories too). You can also search for some recipes based on the nutrients (kcals, proteins, carbs, fat..)

### Sections:

#### 1. Dashboard 

On the dashboard section, you will find, if calculated with other tools on the app, your nutritional goal with explanations and some graphs representing your tracking logs regarding your kcals and workouts.

<img width="1773" alt="Dashboard" src="https://user-images.githubusercontent.com/106601359/184384478-588df2b9-35f1-407a-b0d6-0f2121a5a505.png">


#### 2. Macros

This Section enables you to get your target in terms of kcals and macronutrients after filling out the form. It will also return some explanations about the result. After calculating your macros and kcals, you will be able, if you want, to set this calculation result as your new goal to target by clicking on the "set this result as my new goal" button.

The forms, in order to perform and return the result desired, takes many parameters into account:

* Your gender
* Weight
* Bodyfat
* TEF, how many workout you do/week and the length for each workout
* Your level in the gym
* Your activity level
* Your diet restrictions (vegan or omnivore for example)
* Your diet preferences in terms of macros (high fat low carbs, high carbs low fat or even the default parameters of the app)
* And finally but most important: your goal.

<img width="1781" alt="macros_calculator" src="https://user-images.githubusercontent.com/106601359/184384583-1a2afd07-413b-4fce-a5de-ffde4bac7cef.png">

#### 3. Workout

This section enables your to create your own workout that you will then be able to track in the section "Tracking"

<img width="1785" alt="create_workout" src="https://user-images.githubusercontent.com/106601359/184384634-71f0f265-ab37-441a-8b51-43a23d86c0d9.png">

#### 4. Tracking

This section enables your to track your daily kcals entries and your workouts for the date your choose. That data will be registered and be displayed in two ways;

* First way : On the dashboard, you will se some graphs appear once you start tracking your kcals and your workouts.

* Second way : You can also see what you entered in the section in the Navbar > My account > History.

<img width="1789" alt="track_kcals" src="https://user-images.githubusercontent.com/106601359/184384657-4e0037d7-6ce5-44c6-a533-bf424834997b.png">
<img width="1776" alt="track_workout" src="https://user-images.githubusercontent.com/106601359/184384679-7ff46f45-2766-4973-aa2d-30b00a6fe49f.png">


#### 5. Recipes Discovery

  This section enables your to find some recipes based on kcals and macronutrients desired. You can enter a range for each input needed to perform the search which are :

  * Kcals:  min - max
  * Protein:  min - max
  * Carbs:  min - max
  * Fat:  min - max


  Important; all of the field in the form must be completed, otherwise, the form won't be submitted and therefore, won't return any recipees. 

  For this sections of the app, I used the spoonacular Api and went through 2 "filters". The first one is that the app will search recipe based on the nutrients, but then, will use the ID's of the the result for this first query to do a second query to the api called "Get recipe information" that contains informations about the recipes itself that we then are able to display such as photo, recipe title, url etc..

<img width="1784" alt="look_for_recipe" src="https://user-images.githubusercontent.com/106601359/184384714-76c1e676-ea96-4982-b1af-447e419919d8.png">
<img width="1781" alt="recipe_result" src="https://user-images.githubusercontent.com/106601359/184384738-939eb4ed-11ae-417f-aab0-b9e3fd5cc951.png">


#### 6. My account

On the button my account, you will find 4 sections:

  1. History -> shows 3 tables of history, one for nutritional goals you've set, one for your daily kcals logs and another one for your workouts logs.

  2. Change my password

  3. Close My Account -> basically delete your account and all data related to the account.

  4. Log out

## Installation

## Flask

Click [Here](https://flask.palletsprojects.com/en/2.1.x/installation/) to see how to install Flask


## Running the app

### Install dependencies

In order to run the project, you need to install the dependencies found in the requirements.txt file. 

First you need to install Python if not done already: Click [Here](https://www.python.org/downloads/) to do so.

Then, run the following command to create a Virtual Environment:

```bash
# Create a virtual environment
$ python3 -m venv
```

### Activate your environment
You’ll need to use different syntax for activating the virtual environment depending on which operating system and command shell you’re using.

On Unix or MacOS, using the bash shell: source /path/to/venv/bin/activate<br>
On Unix or MacOS, using the csh shell: source /path/to/venv/bin/activate.csh<br>
On Unix or MacOS, using the fish shell: source /path/to/venv/bin/activate.fish<br>
On Windows using the Command Prompt: path\to\venv\Scripts\activate.bat<br>
On Windows using PowerShell: path\to\venv\Scripts\Activate.ps1<br>

```bash
# After your environment has been activated, install the dependencies
$ pip install -r requirements.txt
```

## Now run the project

```bash
# development
$ flask run

# to enable hot reload, run:
$ export FLASK_ENV=development
```

## You will need a spoonacular API key to run the section "find recipes"

Get your key [Here](https://spoonacular.com/food-api/docs)

After you registered your account for spoonacular, you'll need to insert your key in helpers.py (line 41 & 59)

## Comments
This is my first ever project and I know that It could be improved on every level. But still, I'm proud of what I was able to build after only taking the course CS50x and doing some research on the internet! Thank David J. Malan and every other people from the Team of CS50. 


## Stay in touch

- Author - [Marcello](https://github.com/Marxi7)

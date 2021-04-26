from cmu_112_graphics import *
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn import tree
'''learned how to use sklearn functions using these functions
1) this is where I learned how to structure the learning and predicting model in code
https://randerson112358.medium.com/python-logistic-regression-program-5e1b32f964db
2) this is where I learned about the function used in the project 
https://scikit-learn.org/stable/modules/tree.html#classification
'''
y  = pd.read_csv("test.csv", usecols=['mood']) 
X = pd.read_csv("test.csv", usecols=['day', "time"]) 
#learned to read the csv with https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = tree.DecisionTreeClassifier()
model.fit(x_train, y_train) #Training the model
predictions = model.predict(x_test)
print("PREDICTIONS")
print(x_test)
print(predictions)
'''

y  = pd.read_csv("test.csv", usecols=['mood']) 
X = pd.read_csv("test.csv", usecols=['day', "time"]) 

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression()
model.fit(x_train, y_train) #Training the model
predictions = model.predict(x_test)

print("PREDICTIONS")
print(x_test)
print(predictions)# printing predictions

print()# Printing new line

#Check precision, recall, f1-score
print( classification_report(y_test, predictions) )

print( accuracy_score(y_test, predictions))
'''
def appStarted(app):
    app.days = ['sun', 'mon', 'tue', 'wed', 'th', 'fri', 'sat']
    app.times = range(1, 25)
    app.dayNum = 0
    app.selectItem = "days"
    app.selectItemIndexDays = 0
    app.selectItemIndexTime = 0
    app.result = ""
    print(app.selectItem)

def keyPressed(app, event):
    if event.key == "Left":
        app.selectItem = "days"
    elif event.key == "Right":
        app.selectItem = "times"
    elif event.key == "Up":
        if app.selectItem == "days" and app.selectItemIndexDays + 1 < len(app.days):
            app.selectItemIndexDays = app.selectItemIndexDays + 1
        elif app.selectItem == "times" and app.selectItemIndexTime + 1 < len(app.times):
            app.selectItemIndexTime = (app.selectItemIndexTime + 1)
    elif event.key == "Down":
        if app.selectItem == "days" and app.selectItemIndexDays > 0:
            app.selectItemIndexDays = app.selectItemIndexDays - 1
        elif app.selectItem == "times" and app.selectItemIndexTime > 0:
            app.selectItemIndexTime = (app.selectItemIndexTime - 1) 
    elif event.key == "Enter":
        print(app.selectItemIndexDays + 1)
        print(app.selectItemIndexTime)
        d = {'day': [app.selectItemIndexDays + 1], 'time': [app.times[app.selectItemIndexTime]]}
        x = pd.DataFrame(data=d)
        #https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
        app.result = model.predict(x)[0]

def draw_days(app, canvas):
    x0 = 100
    y0 = 100
    x1 = 200
    y1 = 200
    if app.selectItem == "days":
        canvas.create_rectangle(x0, y0, x1, y1, fill="yellow")
    canvas.create_text(x0 + (x1 -x0)/2, y0 + (y1 - y0) /2, text=app.days[app.selectItemIndexDays])
    canvas.create_text(x0 + 20, y0, text="day", anchor="nw")

def draw_times(app, canvas):
    x0 = 200
    y0 = 100
    x1 = 300
    y1 = 200
    if app.selectItem == "times":
        canvas.create_rectangle(x0, y0, x1, y1, fill="yellow")
    canvas.create_text(x0 + (x1 -x0)/2, y0 + (y1 - y0) /2, text=app.times[app.selectItemIndexTime])
    canvas.create_text(x0 + 20, y0, text="time", anchor="nw")

def draw_result(app, canvas):
    x0 = 300
    y0 = 100
    x1 = 400
    y1 = 200
    canvas.create_rectangle(x0, y0, x1, y1, fill="pink")
    canvas.create_text(x0 + (x1 -x0)/2, y0 + (y1 - y0) /2, text=app.result)
    canvas.create_text(x0 + 20, y0, text="mood", anchor="nw")

def redrawAll(app, canvas):
    draw_days(app, canvas)
    draw_times(app, canvas)
    draw_result(app, canvas)

runApp(width=500, height=500)

'''
iris_data = load_iris()
X, y = pd.DataFrame(data=iris_data.data, columns=iris_data.feature_names), pd.DataFrame(data=iris_data.target, columns=["iris_type"])
print(X.head())
print(y.head())
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression()
model.fit(x_train, y_train) #Training the model
predictions = model.predict(x_test)

print("PREDICTIONS")
print(x_test)
print(predictions)# printing predictions

print()# Printing new line

#Check precision, recall, f1-score
print( classification_report(y_test, predictions) )

print( accuracy_score(y_test, predictions))'''
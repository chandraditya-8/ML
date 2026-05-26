from flask import Flask, request, render_template_string
import pandas as pd
import joblib

app = Flask(__name__)

model = joblib.load('diet_model.pkl')

df = pd.read_csv('data/nutrition.csv')
df.columns = df.columns.str.lower().str.strip()

foods = sorted(df['food_name'].unique())

HTML = '''

<!DOCTYPE html>

<html>

<head>

<title>AI Diet Predictor</title>

<style>

body{
    font-family:Arial;
    background:#f4f7fb;
    padding:40px;
}

.container{
    max-width:700px;
    margin:auto;
    background:white;
    padding:30px;
    border-radius:12px;
    box-shadow:0 0 10px rgba(0,0,0,0.1);
}

h1{
    text-align:center;
    color:#333;
}

select,input,button{
    width:100%;
    padding:12px;
    margin-top:10px;
    border-radius:8px;
    border:1px solid #ccc;
}

button{
    background:#2d89ef;
    color:white;
    border:none;
    font-size:16px;
    cursor:pointer;
}

table{
    width:100%;
    margin-top:20px;
    border-collapse:collapse;
}

th,td{
    border:1px solid #ddd;
    padding:12px;
    text-align:center;
}

th{
    background:#2d89ef;
    color:white;
}

.risk{
    font-size:20px;
    font-weight:bold;
    text-align:center;
    margin-top:20px;
}

</style>

</head>

<body>

<div class="container">

<h1>🥗 AI Diet Health Predictor</h1>

<form method="POST">

<select name="food1">
{% for food in foods %}
<option>{{ food }}</option>
{% endfor %}
</select>

<input type="number" name="qty1" placeholder="Food 1 Quantity (g)" required>

<select name="food2">
{% for food in foods %}
<option>{{ food }}</option>
{% endfor %}
</select>

<input type="number" name="qty2" placeholder="Food 2 Quantity (g)" required>

<button>Analyze Diet</button>

</form>

{% if result %}

<table>

<tr>
<th>Nutrient</th>
<th>Value</th>
</tr>

{% for k,v in result.items() %}

<tr>
<td>{{ k }}</td>
<td>{{ v }}</td>
</tr>

{% endfor %}

</table>

<div class="risk">

{{ risk }}

</div>

<p><b>Recommendation:</b> {{ recommendation }}</p>

{% endif %}

</div>

</body>

</html>

'''

@app.route('/', methods=['GET', 'POST'])

def home():

    result = risk = recommendation = None

    if request.method == 'POST':

        f1 = df[df['food_name'] == request.form['food1']].iloc[0]
        f2 = df[df['food_name'] == request.form['food2']].iloc[0]

        q1 = float(request.form['qty1']) / 100
        q2 = float(request.form['qty2']) / 100

        protein = round(f1['protein']*q1 + f2['protein']*q2,2)
        carbs = round(f1['carbs']*q1 + f2['carbs']*q2,2)
        fat = round(f1['fat']*q1 + f2['fat']*q2,2)
        iron = round(f1['iron']*q1 + f2['iron']*q2,2)
        vitamin = round(f1['vitamin_c']*q1 + f2['vitamin_c']*q2,2)

        pred = model.predict([[protein, carbs, fat, iron]])[0]

        calories = round(pred[0],2)

        result = {
            'Calories': calories,
            'Protein': protein,
            'Carbs': carbs,
            'Fat': fat,
            'Iron': iron,
            'Vitamin C': vitamin
        }

        risk = "✅ Healthy Diet"

        recommendation = "Balanced nutrition intake"

        if calories > 900 or fat > 35:
            risk = "⚠️ High Health Risk"
            recommendation = "Reduce oily food and portion size"

        elif calories > 600:
            risk = "🟡 Moderate Health Risk"
            recommendation = "Maintain balanced quantity"

        if protein < 15:
            recommendation += " | Increase protein intake"

        if vitamin < 20:
            recommendation += " | Add fruits and vegetables"

    return render_template_string(
        HTML,
        foods=foods,
        result=result,
        risk=risk,
        recommendation=recommendation
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
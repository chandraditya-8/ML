from flask import Flask, request, render_template_string
import pandas as pd

app = Flask(__name__)

df = pd.read_csv('data/nutrition.csv')
df.columns = df.columns.str.lower()

food_col = df.columns[0]
foods = sorted(df[food_col].astype(str).unique())

HTML = '''

<h1>🍔 NutriPredict</h1>

<form method="POST">

<input name="food" list="foods" placeholder="Food Name" required>

<datalist id="foods">
{% for food in foods %}
<option value="{{ food }}">
{% endfor %}
</datalist>

<input name="quantity" type="number" placeholder="Quantity (g)" required>

<button>Get Nutrition</button>

</form>

{% if result %}

<table border="1" cellpadding="10">

{% for k,v in result.items() %}

<tr>
<td>{{ k }}</td>
<td>{{ v }}</td>
</tr>

{% endfor %}

</table>

{% endif %}

'''

@app.route('/', methods=['GET', 'POST'])

def home():

    result = None

    if request.method == 'POST':

        food = request.form['food'].lower()
        qty = float(request.form['quantity'])

        row = df[
            df[food_col].astype(str).str.lower() == food
        ]

        if not row.empty:

            row = row.iloc[0]

            result = {}

            for col in df.columns:

                val = row[col]

                try:
                    val = round(float(val) * qty / 100, 2)
                except:
                    pass

                result[col] = val

    return render_template_string(
        HTML,
        result=result,
        foods=foods
    )

if __name__ == '__main__':
    app.run(debug=True)
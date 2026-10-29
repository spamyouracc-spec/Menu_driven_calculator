from flask import Flask, render_template_string, request

app = Flask(__name__)

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None
    if request.method == "POST":
        try:
            num1 = float(request.form["num1"])
            num2 = float(request.form["num2"])
            operation = request.form["operation"]

            if operation == "add":
                result = add(num1, num2)
            elif operation == "subtract":
                result = subtract(num1, num2)
            elif operation == "multiply":
                result = multiply(num1, num2)
            elif operation == "divide":
                result = divide(num1, num2)
            else:
                error = "Invalid operation"
        except ValueError as e:
            error = str(e)

    return render_template_string("""
    <!doctype html>
    <html>
    <head>
      <title>Calculator</title>
      <style>
        body { font-family: Arial; margin: 50px; }
        form { max-width: 300px; }
        input, select, button { display: block; width: 100%; margin: 10px 0; padding: 8px; }
      </style>
    </head>
    <body>
      <h1>Menu-Driven Calculator</h1>
      <form method="post">
        <label>Number 1</label>
        <input type="number" step="any" name="num1" required>
        <label>Number 2</label>
        <input type="number" step="any" name="num2" required>
        <label>Operation</label>
        <select name="operation">
          <option value="add">Addition</option>
          <option value="subtract">Subtraction</option>
          <option value="multiply">Multiplication</option>
          <option value="divide">Division</option>
        </select>
        <button type="submit">Calculate</button>
      </form>

      {% if result is not none %}
        <h2>Result: {{ result }}</h2>
      {% endif %}
      {% if error %}
        <h3 style="color:red;">{{ error }}</h3>
      {% endif %}
    </body>
    </html>
    """, result=result, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

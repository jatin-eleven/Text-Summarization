
from flask import Flask, render_template, url_for, redirect, jsonify, request
from ml_script import Text_Summarization


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == "POST":
        text = request.form['title']
        print(text)
        # try : 
        result = Text_Summarization(str(text))
        print(result)
        if len(result) == 0:
            result = "e"
        # except :
            # print("Error Generated Somewhere")
            # result = "ee"
        return render_template("index.html", result=result, text=text)

    return render_template("index.html")





if __name__ == '__main__':
  app.run(debug=True, port = 5111)
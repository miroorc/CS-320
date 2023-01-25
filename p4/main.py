# project: p4
# submitter: mchoi82
# partner: none
# hours: 48
import pandas as pd
import re
import flask
from flask import Flask, request, jsonify
import time
import matplotlib.pyplot as plt
import io
import csv
import matplotlib as pltt
pltt.use("Agg")

#data is from https://dhsgis.page.link/pb5Z  "Wisconsin COVID-19 Historical Data Downloads"

app = Flask(__name__)

df = pd.read_csv("main.csv")

@app.route('/browse.html') #dynamic: page doesnt correspond to a file
def browse_handler():
    # csv to html code by GeeksforGeeks --> https://www.geeksforgeeks.org/convert-csv-to-html-table-in-python/
    import pandas as pd

    # to read csv file named "samplee"
    df = pd.read_csv("main.csv")
    html_file = df.to_html()  
    var = "<html><body><h1>Browse</h1></body></html>"
    
    return var + html_file




last_visit = 0
dic = {}
@app.route('/browse.json') #dynamic: page doesnt correspond to a file
def browse_json():
    global last_visit
    global dic
    ip = flask.request.remote_addr
    if ip in dic and time.time() - dic[ip] < 60:
            return flask.Response("<b>too many requests. Try next time</b>", status = 429,
                                  headers = {"Retry-After":"60"})
    elif ip in dic and time.time() - dic[ip] >= 60 or ip not in dic:
        dic[ip] = time.time()
        df = pd.read_csv("main.csv")
        dic_file = df.to_dict('index')
        return dic_file


    
@app.route('/visitors.json') #dynamic: page doesnt correspond to a file
def browse_visitors():
    global dic
    return list(dic.keys())

    

donate_a = 0
donate_b = 0

@app.route('/donate.html')
def donate():
    global donate_a
    global donate_b
    args = dict(flask.request.args)
    try:
        adr = args['from']
    except KeyError:
        return '<html><body><h1>please specify from</h1></body></html>'
    
    if adr == 'a':
        donate_a += 1
    elif adr == 'b':
        donate_b += 1
        
    return """<html><body style="background-color:lightblue">
               <h1> We need your help! </h1>
                Please Kindly Donate Here!
               <body></html>"""


num_subscribed = 0
@app.route('/email', methods=["POST"])
def email():
    global num_subscribed
    email = str(request.data, "utf-8")  #[a-z]{3}
    if len(re.findall(r"^[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]{2,3}$", email)) > 0: # 1
        with open("emails.txt", "a") as f: # open file in append mode
            f.write(email + '\n') # 2
        num_subscribed += 1
        return jsonify(f"thank you, you're subscriber number {num_subscribed}!")
    return jsonify("please double check the email address before submitting!") # 3



@app.route("/plot1.svg")
def plot1():
    fig, ax = plt.subplots(figsize = (4,4))
    df.plot.line("NEG", "NEG_NEW", ax=ax)
    ax.set_ylabel("NEG_NEW")
    ax.set_title("Negative vs New Negative")
    
    f = io.StringIO()
    fig.savefig(f, format = "svg")
    plt.close()
    return flask.Response(f.getvalue(), headers = {"Content-Type": "image/svg+xml"})


@app.route("/plot2.svg")
def plot2():
    args = int(flask.request.args.get("bins", 10))
    fig, ax = plt.subplots(figsize = (4,4))
    df["NEG_7DAYAVG"].hist(ax = ax, bins = args)
  
    ax.set_ylabel("Negative Cases(7Days avg)")
    ax.set_xlabel("Negative Cases#")
    ax.set_title("Negative vs 7 Days avg Negative")
    
    f = io.StringIO()
    fig.savefig(f, format = "svg")
    plt.close()
    return flask.Response(f.getvalue(), headers = {"Content-Type": "image/svg+xml"})

    

home_visit = 0
@app.route('/')
def home():# static file
    global home_visit
    home_visit += 1
    if home_visit <= 10 and home_visit % 2 == 0:
        with open("index_a.html") as f:
            html = f.read()
            
    elif home_visit <= 10 and home_visit % 2 != 0:
        with open("index_b.html") as f:
            html = f.read()
    
    elif home_visit > 10:
        if donate_a > donate_b:
            with open("index_a.html") as f:
                html = f.read()
        else:
            with open("index_b.html") as f:
                html = f.read()
            
    
    return html



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False) # don't change this line!

# NOTE: app.run never returns (it runs for ever, unless you kill the process)
# Thus, don't define any functions after the app.run call, because it will
# never get that far.




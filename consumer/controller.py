from flask import Flask,request,render_template
from consumer.consume_service import *
from consumer.product import Prod

app = Flask(__name__)

def dummyprod():
    return Prod(pid=0,pnm='',pqty=0,pri=0.0)

@app.route("/consumer/welcome/")
def welcome_page():
    return render_template('product.html',
                           products = get_all_products(),
                           product = dummyprod())

@app.route("/consumer/save/",methods=["post"])
def save_or_update():
    dbprod = get_product(request.form["pid"])
    prodinfo = Prod(pid=request.form["pid"],
         pnm=request.form["pnm"],
         pqty=request.form["pqty"],
         pri=request.form["ppri"])
    msg = "AAAAA"
    if type(dbprod)==Prod:
        msg = update_product(prodinfo)
    else:
        msg = add_product(prodinfo)

    print(msg)
    if msg.get("pname")==None and msg.get("pqty")==None and msg.get("pprice")==None:
        prodinfo = dummyprod()

    #if "Saved" in msg.get("status") or 'Updated' in msg.get("status"):
    #    prodinfo = dummyprod()

    return render_template('product.html',msg=msg,
                           products=get_all_products(),
                           product=prodinfo)

@app.route("/consumer/edit/<int:pid>")
def fetch_for_edit(pid):
    return render_template('product.html',
                           products=get_all_products(),
                           product=get_product(pid))

@app.route("/consumer/delete/<int:pid>")
def delete_product_consumer(pid):
    msg = delete_product(pid)
    return render_template('product.html',msg=msg,
                           products=get_all_products(),
                           product=dummyprod())



if __name__ == '__main__':
    app.run(debug=True,port=5001)
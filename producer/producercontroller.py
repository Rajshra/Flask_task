
from flask import Flask,request as req
from producer.model import *
import json

def apply_business_constraints(prodinfo):
    pname = prodinfo["pnm"]
    pqty = prodinfo["pqty"]
    pprice = prodinfo["ppri"]
    dictOfErrors = {}
    if len(pname)<4:
        dictOfErrors["pname"]="Product Name length shud be atleast 5 chars"
    if pqty<2:
        dictOfErrors["pqty"] = "Atleast 2 quantites expected for the product"
    if pprice<100:
        dictOfErrors["pprice"] = "Atleast product price should be INR 100 "

    return dictOfErrors


db.create_all()

@app.route("/producer/product/",methods=["POST"])
def create_product():
    prodinfo = req.get_json()

    errors = apply_business_constraints(prodinfo)
    if errors:
        return json.dumps(errors)

    prodmodel = Product(pname=prodinfo["pnm"],
            pqty=prodinfo["pqty"],
            pprice=prodinfo["ppri"])
    db.session.add(prodmodel)
    db.session.commit()
    return {"status":"Product < {} > Saved Successfully....!".format(prodmodel.id)}

def remove_not_serializable_field(prod):
    prod.__dict__.pop('_sa_instance_state')
    prod.__dict__.pop('active')
    return prod

@app.route("/producer/product/",methods=["GET"])
def get_all_products():
    products = Product.query.all()
    if products:
        activeProducts = []
        for prod in products:
            if prod.active=='Y':
                prod = remove_not_serializable_field(prod)
                activeProducts.append(prod.__dict__)
        return json.dumps(activeProducts)
    else:
        return {"status":"No products avaiable"}

@app.route("/producer/product/<int:pid>",methods=["DELETE"])
def delete_product(pid):
    dbprod = Product.query.filter_by(id=pid).first()
    msg = "Product Deleted Successfully....!"
    if dbprod:
        dbprod.active='N'
        db.session.commit()
    else:
        msg = "Product Not Avaiable so cannot delete...!"
    return {"status" : msg}

@app.route("/producer/product/<int:pid>",methods=["PUT"])
def update_product(pid):
    dbprod = Product.query.filter_by(id=pid).first()
    msg = "Product Updated Successfully....!"
    prodinfo = req.get_json()

    errors = apply_business_constraints(prodinfo)
    if errors:
        return json.dumps(errors)

    if dbprod:
        dbprod.pname=prodinfo["pnm"]
        dbprod.pqty = prodinfo["pqty"]
        dbprod.pprice = prodinfo["ppri"]
        db.session.commit()
    else:
        msg = "Product Not Avaiable so cannot update...!"
    return {"status": msg}


@app.route("/producer/product/<int:pid>",methods=["GET"])
def get_single_product(pid):
    dbprod = Product.query.filter_by(id=pid).first()
    if dbprod and dbprod.active=='Y':
        dbprod = remove_not_serializable_field(dbprod)
        return json.dumps(dbprod.__dict__)
    else:
        return {"status" : "Product With Given Id not avaiable..!"}


if __name__ == '__main__':
    app.run(debug=True,port=5000)



from consumer.product import Prod
import requests as reqs

msg = "Product Saved Successfully.."


BASE_URI="http://localhost:5000/producer/product/"



def convertToProdJson(prod):
    prod_json = {
        "pnm" : prod.productName,
        "pqty" : prod.productQty,
        "ppri" : prod.productPrice
    }
    print(prod_json)
    return prod_json


def convertToProduct(pjson):
    return Prod(pid=pjson["id"],pnm=pjson["pname"],
                pqty=pjson["pqty"],
         pri=pjson["pprice"])
def deserialize(pjsons):
    if pjsons.__contains__('status'):
        return pjsons["status"]

    if type(pjsons)==list:#all
        products = []
        for pjson in pjsons:
            products.append(convertToProduct(pjson))
        return products
    else:
        return convertToProduct(pjsons)#single

def get_all_products():
    response = reqs.get(BASE_URI)
    return deserialize(response.json())


def get_product(pid):
    response = reqs.get(BASE_URI+str(pid))
    return deserialize(response.json())

def delete_product(pid):
    response = reqs.delete(BASE_URI+str(pid))
    return response.json()["status"]

def update_product(prod):
    response = reqs.put(BASE_URI+str(prod.productId), json=convertToProdJson(prod))
    print(response.status_code)
    if response.json().__contains__('status'):
        return response.json()
    else:
        #print(response.json())
        return response.json()


def add_product(prod):
    response = reqs.post(BASE_URI,json=convertToProdJson(prod))
    print(response.status_code)
    if response.json().__contains__('status'):
        return response.json()
    else:
        #print(response.json())
        return response.json()


if __name__ == '__main__':
    prod = Prod(pid=7,pnm='ATAYYAFF',pqty=11,pri=223.4)
    #convertToProdJson(prod)
    #print(update_product(prod))
    #print(delete_product(7))
    print(get_product(5))
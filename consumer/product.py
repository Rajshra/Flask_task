

class Prod:

    def __init__(self,pid,pnm,pqty,pri):
        self.productId=int(pid)
        self.productName=pnm
        self.productPrice=float(pri)
        self.productQty=int(pqty)

    def __str__(self):
        return f'''
            Id :{self.productId}
            Name :{self.productPrice}
            Qty : {self.productQty}
            Price : {self.productPrice}
            '''

    def __repr__(self):
        return str(self)

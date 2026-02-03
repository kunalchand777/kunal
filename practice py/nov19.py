class kunal:
    price=100

    def __init__(self,price):
        self.price=price
    def hello(self):
        name="kunal and lucifer"
        return "hello",name
k=kunal()
print(k.hello())
print(k.price)

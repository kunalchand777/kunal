class Car:
    def __init__(self):
     self.__acc=False
     self.__speed=False
     self.__stop=False
     
    def start(self):
        self.__acc=True
        self.__speed=True
        self.__stop=False
        print("car started")
        print("car is running at speed ",self.__speed)
        print("car is accelarating ",self.__acc)
        print("car is stopped ",self.__stop)
         
car=Car()
car.start()
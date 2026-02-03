class Car:
 color="black"
 @staticmethod
 def start():
     print("car started")
     
@staticmethod
def stop():
 print("car stopped")
class porschecar(car):
  def __init__(self, name):
    self.name=name
    car1= porschecar("porsche")
    car1.start()
    print("car color is " + car1.color)
    car1.stop()
    
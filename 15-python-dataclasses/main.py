from dataclasses import dataclass
from typing import ClassVar

@dataclass
class Pakistani:
    name:str
    age:int
    profession:str
    arms:ClassVar[int] = 4    
    
    def eat(self):
        return f"{self.name} eats biryani."    
    
    @staticmethod
    def has_arms():
        return f"He Has {Pakistani.arms} arms"
    
yaseen = Pakistani("Yaseen",22,"Electrical Engineer")
print(yaseen)
print(yaseen.name)
print(yaseen.age)
print(yaseen.profession)
print(yaseen.eat())
print(Pakistani.has_arms())
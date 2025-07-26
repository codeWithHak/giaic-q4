def get_user_data(age:int,salary:int):    
    user_data = [
    
        {"name":"Huzair Ahmed Khan", "age":19, "salary":1500000},
    
        {"name":"Huzaifa Farooqui", "age":26, "salary":500000},
    
        {"name":"Shah Rukh Khan", "age":52, "salary":150000000}
    
    ]
    
    for user in user_data:
        if user["age"] > age and user["salary"] < salary:
            user_data.remove(user)
    return user_data            

print(get_user_data(25, 1000000))
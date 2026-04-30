calculations_to_unit = 365
name_of_unit = "days"
time = "years are"


def days_to_unit(num_of_days):
    return(f"{num_of_days} {time} {num_of_days*calculations_to_unit} {name_of_unit}")
    
    

def validate_not_allowed():
    try:
    
        user_input_numb = int(days_to_unit_dictionary)
        if user_input_numb > 50:
             calculation_of_age = days_to_unit(user_input_numb)
             print(calculation_of_age)
        elif user_input_numb == 50:
             print("you're incorrect, make sure you're typing in the correct answer")
 
    except:
       print("try again to get it right")
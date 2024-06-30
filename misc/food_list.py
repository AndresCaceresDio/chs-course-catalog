# Program that prompts a user for a list of foods
# When the user enters "Done", it prints out the food list

def food_list():
    list = []
    while True:
        response = input("Name a food: ")
        if response == "Done":
            print(list)
            break
        else:
            list.append(response)

if __name__ == "__main__":
    food_list()

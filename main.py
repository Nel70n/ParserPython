from ParserGoogle import ParseLink


FlagSession = True

print("*---------------------------------*")
print("|   Pre testing parsing program   |")
print("|                    ver. 0.1.2   |")
print("| author:                         |")
print("|           Trofimov Nikita       |")
print("*---------------------------------*")


while FlagSession:
    try: 
        print('--> ', end="")
        console_input = input()
        print(console_input)
        if console_input == "fi": 
            print("Enter parameters for parse:\n    (query, name file, number of page)")
            parameters = list(input().split(", "))
            # parameters = ['Elon Musk', 'Elon Musk', 3] # <-- Пример ввода 
            print(f"Query: {parameters[0]}\nFile: {parameters[1] + '.csv'}\nCount Page: {parameters[2]}")

            session = ParseLink()
            session.ParseQuery(
                query = parameters[0], 
                name_file = parameters[1] + ".csv", 
                count_pages = int(parameters[2])
            )

        elif console_input == "pc":
            print("Enter name file (with .csv): ", end = "")
            name_file = input()
            session = ParseLink()
            session.ParseNewsSite(
                name_file = name_file
            )

        elif console_input == 'exit':
            FlagSession = False

        elif console_input == 'Help':
            print("*--------------------------------------*")
            print("| fi – find information from news site |")
            print("| exit|ex – exit from program          |")
            print("*--------------------------------------*")

        elif console_input == "^C":
            FlagSession = False

    except KeyboardInterrupt:
        break
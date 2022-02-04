from ParserGoogle import ParseLink

flag = True

print("*---------------------------------*")
print("|   Pre testing parsing program   |")
print("|                    ver. 0.0.1   |")
print("| author:                         |")
print("|           Trofimov Nikita       |")
print("*---------------------------------*")


while flag:
    try: 
        print('--> ', end="")
        console_input = input()
        if console_input == 'find file':
            print("[*] Edit query:", end=" ")
            query = input()

            print("[*] File for search:", end=" ")
            type_doc = input()

            print("[*] Remove site:", end=" ")
            site = input()

            print("[*] Enter file for save:", end=" ")
            name_file = input() + ".csv"

            session = ParseLink()
            session.CreateQuery(
                query=query,
                type_doc=type_doc,
                site=site
            )
            session.CreateResponse(
                name_file = name_file
            )
        elif console_input == 'exit':
            flag = False
        elif console_input == 'Help':
            print("*-----------------------------------*")
            print("| find file – find files from query |")
            print("| exit – exit from program          |")
            print("*-----------------------------------*")

    except KeyboardInterrupt:
        break
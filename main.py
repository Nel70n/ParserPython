from ParserGoogle import ParseLink

flag = True
print("*---------------------------------*")
print("|   Pre testing parsing program   |")
print("|                    ver. 0.0.1   |")
print("| author:                         |")
print("|         Trofimov Nikita         |")
print("*---------------------------------*")
while flag:
    try: 
        print('--> ', end="")
        console_input = input()
        if console_input == 'find file':
            print("[*] Edit query:", end=" ")
            query = input()
            session = ParseLink(
                query=query
            )
            session.CreateResponse()
        elif console_input == 'exit':
            flag = False
        elif console_input == 'Help':
            print("*-----------------------------------*")
            print("| find file – find files from query |")
            print("| exit – exit from program          |")
            print("*-----------------------------------*")

    except KeyboardInterrupt:
        break
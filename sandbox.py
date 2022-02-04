from time import sleep


print("Hello!")
print ("\033[A\033[A")

print('DUDU')

for i in range(101):
    print(str(i)+"%")
    sleep(1)
    print ("\033[A\033[A")

class waiting:
    def __init__(self) -> None:
        pass
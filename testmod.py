import wifsm

Axel = wifsm.User(0)

Axel2 = wifsm.User(1)

dict1 = str(Axel.getCalendarEvents())
dict2 = str(Axel2.getCalendarEvents())

print(dict1 + "\n")
print(dict2 + "\n")

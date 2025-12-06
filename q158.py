cpu = [10, 40, 65, 95]
for usage in cpu:
    if usage <= 20:
        status = "Idle"
    elif usage <= 60:
        status = "Normal"
    elif usage <= 80:
        status = "Busy"
    else:
        status = "Overloaded"
        
print("Category:", status)
print(usage, "→", status)





    
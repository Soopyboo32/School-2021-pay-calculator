#--------------------------------------------------------
#      NOTE: This is ONLY for the trace table
#            as that would be unfeasable in
#            the other version.
#--------------------------------------------------------

#Static arrays describing day information
Days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
BaseRate = [1.0,1.0,1.0,1.0,1.0,1.5,1.5]
OverTimePercentUnder3 = [1.25,1.25,1.25,1.25,1.25,1.5,1.5]
OverTimePercentOver3 = [1.45,1.45,1.45,1.45,1.45,1.5,1.5]
BonusPay = [0.0,0.0,0.0,0.0,0.0,4.0,4.0]
DayRegularHours = [8.0,8.0,8.0,8.0,8.0,8.0,8.0]

TotalPay = 0

EmployeePay = float(input("Employee wage ($/h)? : "))

#Main loop over Days
for dayId in range(7):
    print("How many hours did the employee work on " + Days[dayId] + "?")
    time = max(0, min(24, float(input(": "))))# min and maxes act as a clamp around valid range

    DailyWage = EmployeePay+BonusPay[dayId]

    BaseRateHours = min(time, 8)
    Under3hOverTime = max(0, min(time-BaseRateHours, 3))
    Over3hOverTime = max(0,time-BaseRateHours-Under3hOverTime)

    TotalPay = TotalPay + BaseRateHours*BaseRate[dayId]*DailyWage + Under3hOverTime*OverTimePercentUnder3[dayId]*DailyWage + Over3hOverTime*OverTimePercentOver3[dayId]*DailyWage

print("They made $" + str(TotalPay) + " this week!")
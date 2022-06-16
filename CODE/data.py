from settings import Settings
from language import Translator

class InteractDataClass:
    def __init__(self):
        #do stuf
        self.currStorageId = 0
        self.dataStorages = {}

        Settings.interactData = self

    def newEmployeeFile(self):
        #do stuff

        storage = DataStorage(self.currStorageId)

        storage.isEmployeeFileSaved = False

        self.currStorageId += 1

        self.dataStorages[storage.thisId] = storage

        return storage
    
    def getWeekDayIds(self):
        return [0, 1, 2, 3, 4, 5, 6] # can change order in settings maby later
    
    def getDayNameFromId(self, dayId):
        return Translator.translateComponent("week.day." + str(dayId))

    def loadFromJSON(self, json):
        storage = DataStorage(self.currStorageId)

        storage.isEmployeeFileSaved = True

        self.currStorageId += 1

        self.dataStorages[storage.thisId] = storage

        storage.currMaxEmployeeId = json["currMaxEmployeeId"]
        storage.currMaxJobPositionId = json["currMaxJobPositionId"]

        for id in json["jobPositions"].keys(): #add job positions first, as employees require resolving a job position from id
            tempPos = JobPosition()
            tempPos.parentData = storage
            tempPos.loadFromJSON(json["jobPositions"][id])
            storage.jobPositions[id] = tempPos

        for id in json["employees"].keys():
            tempEmp = Employee()
            tempEmp.parentData = storage
            tempEmp.loadFromJSON(json["employees"][id])
            storage.employees[id] = tempEmp

        storage.updateCalculations()

        return storage

class DataStorage:
    def __init__(self, id):
        #Class that stores the data
        self.jobPositions = {}#hashmap from positionId to position class
        self.employees = {}#hashmap from employeeId to employee class

        self.currMaxEmployeeId = 0
        self.currMaxJobPositionId = 0

        self.thisId = id

        self.isEmployeeFileSaved = False
        self.filename = None
        self.fileLocationFull = None

        self.parentTab = None


    def setParentTab(self, parentTab):
        self.parentTab = parentTab
        self.updateCalculations()

    def addEmployee(self, employee):
        self.currMaxEmployeeId += 1

        employee._setId(self.currMaxEmployeeId)

        employee.parentData = self

        self.employees[str(self.currMaxEmployeeId)] = employee

        self.updateCalculations()

        return employee
    def deleteEmployee(self, employee):
        del self.employees[str(employee.getId())]
    def deletePosition(self, pos):
        del self.jobPositions[str(pos.getId())]

    def getEmployeeFromId(self, id):
        return self.employees[str(id)]
    def getJobFromId(self, id):
        return self.jobPositions[str(id)]
    def getEmployeeIds(self):
        return self.employees.keys()
    def addJobPosition(self, jobPosition):
        self.currMaxJobPositionId += 1

        jobPosition._setId(self.currMaxJobPositionId)

        jobPosition.parentData = self

        self.jobPositions[str(self.currMaxJobPositionId)] = jobPosition

        self.updateCalculations()

        return jobPosition

    def getJobPositionIds(self):
        return self.jobPositions.keys()

    def updateCalculations(self):
        if(self.parentTab):
            self.parentTab.updatePay()

    def toJSON(self):
        resObj = {
            "currMaxEmployeeId": self.currMaxEmployeeId,
            "currMaxJobPositionId": self.currMaxJobPositionId,
            "employees": {

            },
            "jobPositions": {

            }
        }

        for id in self.getEmployeeIds():
            resObj["employees"][id] = self.getEmployeeFromId(id).toJSON()
        
        for id in self.getJobPositionIds():
            resObj["jobPositions"][id] = self.getJobFromId(id).toJSON()

        return resObj

class Employee:
    def __init__(self):
        #stores employee data
        self.hoursWorked = {"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0}#hashmap from dayId to worked hours
        self.name = None
        self.id = None #should be set as soon as this is added to the DataStorage
        self.customPay = None#if none it uses the default jobposition pay
        self.bonus = 0
        self.parentData = None
        
        #the class of the job position,
        self.jobPosition = None

    def _setId(self, id):
        self.id = id
    
    def getId(self):
        return self.id
        
    def setName(self, name):
        self.name = name
        return self
    
    def getName(self):
        return self.name
    
    def setJobPosition(self, position):
        self.jobPosition = position
        
        if(self.parentData):
            self.parentData.updateCalculations()

        return self;

    def setBonus(self, bonus):
        self.bonus = bonus

        if(self.parentData):
            self.parentData.updateCalculations()
    
    def getBonus(self):
        return self.bonus

    def getPay(self):
        if(self.customPay):
            return self.customPay
        if(self.jobPosition):
            return self.jobPosition.getPay()
        
        return 0
    
    def getPayOnDay(self, dayId):
        res = {
            "hoursWorkedReg": 0,
            "hoursWorkedOverTimeUnder3": 0,
            "hoursWorkedOverTimeOver3": 0,
            "payRate": 0,
            "payReg": 0,
            "payOverTimeUnder3": 0,
            "payOverTimeOver3": 0,
            "pay": 0
        } #Not just the pay so i can have dumping logs in the future
          #Use getPayOnDay(day)["pay"] to get the final pay

        res["hoursWorkedReg"] = min(self.getHoursWorked(dayId), Settings.getDayRegularHours(dayId))
        res["hoursWorkedOverTimeUnder3"] = max(0,min(self.getHoursWorked(dayId)-res["hoursWorkedReg"],3))
        res["hoursWorkedOverTimeOver3"] = max(0,self.getHoursWorked(dayId)-res["hoursWorkedReg"]-res["hoursWorkedOverTimeUnder3"])

        res["payRate"] = self.getPay() + Settings.getDayBonusPay(dayId)

        res["payReg"] = res["payRate"]*Settings.getDayBaseRate(dayId)*res["hoursWorkedReg"]
        res["payOverTimeUnder3"] = res["payRate"]*Settings.getDayOverTimePercentageUnder3(dayId)*res["hoursWorkedOverTimeUnder3"]
        res["payOverTimeOver3"] = res["payRate"]*Settings.getDayOverTimePercentageOver3(dayId)*res["hoursWorkedOverTimeOver3"]

        res["pay"] = res["payReg"]+res["payOverTimeUnder3"]+res["payOverTimeOver3"]
        return res
    
    def getTotalPay(self):
        res = {
            "days": {},
            "bonus": 0,
            "pay": 0
        } #Not just the pay so i can have dumping logs in the future
          #Use getPayOnDay(day).pay to get the final pay

        for dayId in InteractData.getWeekDayIds():
            res["days"][dayId] = self.getPayOnDay(dayId)
            res["pay"] += res["days"][dayId]["pay"]
        
        res["bonus"] = self.getBonus()

        res["pay"] += res["bonus"]
    
        return res

    def getHoursWorked(self, dayId):
        return self.hoursWorked[str(dayId)]

    def setHoursWorked(self, dayId, hours):
        self.hoursWorked[str(dayId)] = hours
        
        if(self.parentData):
            self.parentData.updateCalculations()

    def toJSON(self):
        resObj = {
            "hoursWorked": self.hoursWorked,
            "name": self.name,
            "id": self.id,
            "customPay": self.customPay,
            "bonus": self.bonus,
            "jobPosition": self.jobPosition.getId() if self.jobPosition else -1,
        }

        return resObj
    
    def loadFromJSON(self, json):
        self.hoursWorked = json["hoursWorked"]
        self.name = json["name"]
        self.id = json["id"]
        self.customPay = json["customPay"]
        self.bonus = json["bonus"]
        if(json["jobPosition"] == -1):
            self.jobPosition = None
        else:
            self.jobPosition = self.parentData.getJobFromId(json["jobPosition"])
    
class JobPosition:
    def __init__(self):
        self.pay = 0
        self.name = None
        self.id = None
        self.parentData = None

    def _setId(self, id):
        self.id = id
    
    def getId(self):
        return self.id
        
    def setName(self, name):
        self.name = name
        return self
    
    def setPay(self, pay):
        self.pay = pay
        
        if(self.parentData):
            self.parentData.updateCalculations()
        return self

    def getPay(self):
        return self.pay
    
    def getName(self):
        return self.name

    def toJSON(self):
        resObj = {
            "name": self.name,
            "id": self.id,
            "pay": self.pay
        }

        return resObj
    
    def loadFromJSON(self, json):
        self.name = json["name"]
        self.id = json["id"]
        self.pay = json["pay"]

InteractData = InteractDataClass()
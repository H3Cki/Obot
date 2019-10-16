class BuildExceptions:
    
    class NotEnoughResources(Exception):
        pass
    
    class BuildingQueueBusy(Exception):
        pass
    
    class RequirementsNotMet(Exception):
        pass



class LogInExceptions:
    
    class LogInFailed(Exception):
        pass

class BotExceptions:
    
    class Crash(Exception):
        pass

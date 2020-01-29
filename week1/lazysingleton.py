class LazySingleton:
     __instance = None
     def __init__(self):
             if not LazySingleton.__instance:
                     print("Call __init__ method")
             else:
                     print("Instance already created:", self.getInstance())
     @classmethod
     def getInstance(cls):
             if not cls.__instance:
                     cls.__instance = LazySingleton()
             return cls.__instance

 s = LazySingleton()
 LazySingleton.getInstance()
 s1 = LazySingleton()

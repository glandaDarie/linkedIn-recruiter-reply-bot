class Account_name_controller:
    def __init__(self, xpath : str):
        self.xpath = xpath
    
    @classmethod
    def class_method(cls : callable, instance) -> str:
        return str(instance.xpath) + "something more"

instance = Account_name_controller("somepath/somefile.txt")
print(Account_name_controller.class_method(instance))
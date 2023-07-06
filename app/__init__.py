global control_reference
control_reference={}
dados=[]

class DataStore:
    control_reference={}
    @staticmethod
    def add_to_control_reference(key,value):
        global control_reference
        try:
            DataStore.control_reference[key]=value
        except KeyError as e:
            print(e)
        finally:
            pass
    @staticmethod
    def get_control_refetence():
        return DataStore.control_reference
class DataBase:

    def __init__(self, path: str = "./DATABASE.yaml", **kwargs):

        self.path = path

        for name, value in kwargs.items():

            exec(f"self.{name} = {value}", locals())

        self.element_list = kwargs

    def redata(self, name: str, value) -> None:

        exec(f"self.{name} = {value}", locals())

        self.element_list[name] = eval(f"self.{name}", locals())

a = DataBase(test = 123, name = '"test"')

print(a.__dict__)

a.redata("test", 456)

print(a.__dict__)
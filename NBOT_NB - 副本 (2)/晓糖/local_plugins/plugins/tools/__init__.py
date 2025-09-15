from .tool_file import *

from .tool_exception import *

from .tool_rule import *

from .tool_msg import *


class DataBase:

    """数据库类"""

    def __init__(self, path: str = "./DATABASE.json", post: str = "json", **kwargs) -> None:

        self.path = path

        self.post = post

        if not len(kwargs):

            if not file_exists(path):

                raise Exception
            
            if post == "json":

                kwargs = json_file(path)

            elif post == "yaml":

                kwargs = yaml_file(path)

        for name, value in kwargs.items():

            exec(f"self.{name} = {value}", locals())

        self.element_list = kwargs

    def save(self) -> None:

        if self.post == "json":

            json_file(self.path, self.element_list)

        elif self.post == "yaml":

            yaml_file(self.path, self.element_list)

    def redata(self, name: str, value = None) -> None | Any:

        if value is not None:

            if type(eval(f"self.{name}", locals())) in [list, dict, set, tuple]:

                exec(f"self.{name}.append({value})", locals())

            else:

                exec(f"self.{name} = {value}", locals())
        
            self.element_list[name] = eval(f"self.{name}", locals())

            self.save()

        else:

            return eval(f"self.{name}", locals())
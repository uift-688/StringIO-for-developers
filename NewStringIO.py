from io import StringIO as StrIO
from typing import Union
import sys
from types import FunctionType as Function
import copy

def EmptyFunc(*NoneVar):
    pass

class NewStrIO(StrIO):
    def __handle_output(self, Output):
        args = []
        DefaultNone = False

        FuncArgs = Output["args"]
        Output = Output["return"]
        ExecFunc = None

        for i, IOutput in enumerate(Output):
            try:
                if type(IOutput) != tuple:
                    return []
                for value in IOutput:
                    if value[0] == "super.args":
                        args += list(value[1])
                    elif value[0] == "exec.code":
                        ExecFunc = lambda: exec(value[1], {"__builtins__": __builtins__, "self": self, "args": FuncArgs, **{name: module for name, module in sys.modules.items()}}, {})
                    elif value[0] == "return":
                        return value[1]
                    elif value[0] == "super.default.None":
                        DefaultNone = value[1]
            except Exception as e:
                print(e)
        if DefaultNone:
            args.append("DefaultNone")
        return args, ExecFunc
    
    def __MultiFunction(self, funcs: list, args: list, arkeys: dict) -> list:
        outputs = []
        for value in funcs:
            outputs.append(value(*args, **arkeys))
        print(outputs)
        return outputs
    
    def __MultiHandler(self, data: Union[tuple, Function], args: Union[tuple, None] = None) -> dict:
        if args is None:
            args = ()
        if isinstance(data, Function):
            return {"return": [data(*list(args))], "args": args}
        elif isinstance(data, tuple):
            return {"return": self.__MultiFunction(list(data), list(args), {}), "args": args}

    def __init__(self, initial_value: Union[str, None] = None, newline: Union[str, None] = None, OnWrite = EmptyFunc, OnRead = EmptyFunc, OnSeek = EmptyFunc, OnTell = EmptyFunc, OnClose = EmptyFunc, OnInit = EmptyFunc) -> None:
        self.OnWrite = OnWrite
        self.OnRead = OnRead
        self.OnSeek = OnSeek
        self.OnTell = OnTell
        self.OnClose = OnClose
        self.Writes = []
        self._BaseClass = copy.deepcopy(StrIO)
        super().__init__(initial_value, newline)
        if isinstance(OnInit, (tuple, list)):
            for value in OnInit:
                value(self)
        else:
            OnInit(self)

    def write(self, s: str) -> int:
        Output = self.__MultiHandler(self.OnWrite, (s, ))
        args, Func = self.__handle_output(Output)
        if "DefaultNone" in args:
            s = None
            del args[-1]
        if s is None:
            self.Writes.append(args[0])
            if Func is not None:
                Func()
            return super().write(*args)
        else:
            self.Writes.append(s)
            if Func is not None:
                Func()
            return super().write(*[s, *args])

    def read(self, size: Union[int, None] = None) -> str:
        Output = self.__MultiHandler(self.OnRead, (size, ))
        args = self.__handle_output(Output)
        if "DefaultNone" in args:
            size = None
            del args[-1]
        if size is None:
            return super().read(*args)
        else:
            return super().read(*[size, *args])

    def seek(self, cookie: int, whence: int = 0) -> int:
        Output = self.__MultiHandler(self.OnSeek, (cookie, whence))
        args = self.__handle_output(Output)
        if "DefaultNone" in args:
            cookie, whence = None, None
            del args[-1]
        if (cookie, whence) == (None, None):
            return super().seek(*args)
        else:
            return super().seek(*[cookie, whence, *args])

    def tell(self) -> int:
        Output = self.__MultiHandler(self.OnTell, ())
        args = self.__handle_output(Output)
        if args != []:
            print("Function “super.tell” has no arguments")
        return super().tell()

    def close(self) -> None:
        Output = self.__MultiHandler(self.OnClose, ())
        Output = self.OnClose()
        args = self.__handle_output(Output)
        if args != []:
            print("Function “super.close” has no arguments")
        return super().close()

def SetStdout1(value):
    return (("super.args", (f"{value}\n", )), ("super.default.None", True), ("exec.code", "sys.stdout.write(self.Writes[-1])"))

def SetDefault1(self: NewStrIO):
    self.write("Hello.")

stdout = NewStrIO(OnWrite=(SetStdout1, ), OnInit=(SetDefault1, ))


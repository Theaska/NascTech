from importlib import import_module
from main.exceptions import FunctionNotFound


class FuncClassBase:
    """
        Base class for importing and getting func with func_prefix from module name
    """
    func_prefix = ''
    module_name = None

    def __new__(cls, *args, **kwargs):
        cls._check_module_path()
        return super().__new__(cls)

    @classmethod
    def _check_module_path(cls):
        if not cls.module_name:
            raise ValueError('module_path can not be empty')

    def get_func(self, func_name: str):
        func_name = self.get_full_func_name(func_name)
        module = import_module(self.module_name)
        try:
            return getattr(module, func_name)
        except AttributeError:
            raise FunctionNotFound('function with name {} not found in module {}'.format(func_name, self.module_name))

    def get_full_func_name(self, func_name: str):
        return self.func_prefix + func_name


class FuncClass(FuncClassBase):
    func_prefix = 'fun_'
    module_name = 'main.functions'

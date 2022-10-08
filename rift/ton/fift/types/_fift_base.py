class _FiftBaseType:
    type_: str
    value: str

    def __init__(self):
        pass

    def __load_data__(self, value: str, *args, **kwargs):
        self.value = value

    def __stack_entry__(self):
        return {
            "type": self.__type__(),
            "value": self.value,
        }

    @classmethod
    def __type__(cls) -> str:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f"Fift{self.__type__().capitalize()}{{{self.value}}}"



class EffectMeta(type):
    effect_types = []

    def __new__(cls, name, bases, dict):
        new = super().__new__(cls, name, bases, dict)
        if name != "BaseEffect":
            cls.effect_types.append(new)
        return new


class BaseEffect(metaclass=EffectMeta):
    pass
from enum import Enum,IntEnum
class Promptkey(str, Enum):
    SR_CREATION = "SR_C"


#mater table ids
class PromptkeyDependency(IntEnum):
    Service = 13
    FEMS = 1
    BEMS = 2
    CLS = 3
    LLS = 4
    HWMS =5

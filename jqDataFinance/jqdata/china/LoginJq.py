from jqdata import macro
from jqdatasdk import *
import numpy as np
import pandas as pd

q = query(macro.MAC_MONEY_SUPPLY_YEAR
          ).limit(100)
df = macro.run_query(q)
print(df)
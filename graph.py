import pandas as pd
import matplotlib.cbook as cbook
pd.read_csv("HCCDI Experts - Sheet1").to_dict()
fname = cbook.get_sample_data('msft.csv', asfileobj=False)
with cbook.get_sample_data('msft.csv') as file:
    msft = pd.read_csv(file)
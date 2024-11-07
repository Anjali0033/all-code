import requests
from lxml import html
import pandas as pd
table = []
r = requests.get("https://www.tickertape.in/screener/equity/prebuilt/SCR0005?ref=eq_screener_homepage")
tree = html.fromstring(r.text)
col = (tree.xpath('//tr[@class="jsx-2807940840 "]'))
for i in col:
    table.append({
        "names" : (i.xpath('./td[2]//text()')),
        "Market Cap" : i.xpath('./td[4]//text()')
    })

output_file = "data.csv"
df = pd.DataFrame(table)
df.to_csv(output_file)
    
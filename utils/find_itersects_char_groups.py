import pandas as pd
import utils.exists_ru.exists_ru_columns as exist_ru
import utils.krepmarket.krepmarket_columns as krepmarket

df = pd.read_excel('temp/datasets/krepmarket/krepmarket_normalized.xlsx')

result = { }
for index, row in df.iterrows():
    for aggregate, chars in krepmarket.TARGET_CHARACTERISTICS.items():
        cnt = 0
        for c in chars:
            if not pd.isna(row[c]):
                cnt += 1

        if cnt > 1:
            if aggregate not in result:
                result[aggregate] = set()
            result[aggregate].add(", ".join([c for c in chars if not pd.isna(row[c])]))

for aggr, groups in result.items():
    print("\t" + aggr)
    for gr in groups:
        print(gr)
    print()

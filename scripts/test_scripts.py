import json

with open("data_hub/data/category_map.json") as f:
    signal_map = json.load(f)


signals = ["Funding Insights","Company Growth","Social Media Analytics"]

list_of_signals = []
for signal in signals:
    list_of_signals.extend(signal_map[signal])

print(list_of_signals)

signals_string = ", ".join(signal for signal in list_of_signals)
print(signals_string)
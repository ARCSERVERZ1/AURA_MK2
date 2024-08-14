
import json

label_data = json.loads(open('sanjay_dem_classifier.json').read())


extra_data = {
    "Bills&Payments": [
       "xxxxxx",
       'xxxxxx',
        "yyyy"
    ],
    "Food&Drinks": [
        "PRISM INFOSYS POC",
        "MDP Coffee House Infosys HYD N"
    ]
}

for key  in extra_data:label_data[key] = label_data[key]+extra_data[key]
for key , values in label_data.items():label_data[key] = list(set(values))

print(label_data)

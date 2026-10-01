import os, json, csv

print("--- TEXT-ONLY 0.9827 vs 0.9775 ---")
with open('results/tables/final_results.csv', 'r') as f:
    r = list(csv.DictReader(f))
    for row in r:
        if 'Text-Only' in row['Model'] or 'Text-only' in row['Model']:
            print("final_results.csv:", row['Macro-F1'])

with open('results/tables/main_results.csv', 'r') as f:
    r = list(csv.DictReader(f))
    for row in r:
        if 'Text-Only' in row['Model'] or 'Text-only' in row['Model']:
            print("main_results.csv:", row['Macro-F1'])
            
with open('artifacts/final_results/primary_benchmark.csv', 'r') as f:
    r = list(csv.DictReader(f))
    for row in r:
        if 'Text-Only' in row['Model'] or 'Text-only' in row['Model']:
            print("primary_benchmark.csv:", row['Macro-F1'])

print("\n--- JSON ANALYSIS ---")
data = json.load(open('experiments/final_results.json'))
if isinstance(data, list):
    for d in data:
        if 'Text' in str(d.get('model_name', '')):
            print("List Item:", d.get('model_name'), d.get('macro_f1'))
else:
    for k, v in data.items():
        if isinstance(v, dict):
            if 'Text' in str(v.get('Model')):
                print(k, v)

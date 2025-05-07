import re
import json

result = """
ádfasdfasdf
Response: Solution:ádfsdfasdf
{
    "time_estimate": 3,
    "development_cost": 20000000
}
ádfasdfasdf
    {{ "role_id": 2, "role_name": "Tester", "suggested_count": 2 }}
"""
json_response = re.findall(r'\{[^}]*\}', result)

if json_response:
    json_object = json.loads(json_response[0])  # Convert the first match to a JSON object
    print(f"JSON Object: {json_object}")
else:
    print("No JSON found.")
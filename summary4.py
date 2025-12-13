import yaml, json, os
from collections import Counter
from datetime import datetime

api_files = ["api1.yaml","api2.yaml","api3.yaml","api4.yaml","api5.yaml"]

total_endpoints = 0
methods = Counter()
auth_methods = set()
with_resp = 0
without_resp = 0
resp_codes = set()

for file in api_files:
    if not os.path.exists(file): continue
    data = yaml.safe_load(open(file))
    paths = data.get("paths", {})
    sec = data.get("components", {}).get("securitySchemes", {})
    auth_methods.update(sec.keys())
    for path, ms in paths.items():
        for m, d in ms.items():
            total_endpoints += 1
            methods[m.upper()] += 1
            resp = d.get("responses", {})
            if resp: 
                with_resp += 1
                resp_codes.update(resp.keys())
            else: without_resp += 1

coverage = (with_resp/total_endpoints*100) if total_endpoints else 0

summary = {
    "total_endpoints": total_endpoints,
    "http_method_distribution": dict(methods),
    "authentication_methods": list(auth_methods),
    "endpoints_with_responses": with_resp,
    "endpoints_missing_responses": without_resp,
    "response_codes_encountered": sorted(resp_codes),
    "coverage_percentage": round(coverage,2),
    "generated_at": str(datetime.now())
}

json.dump(summary, open("summary.json","w"), indent=2)

with open("README_analysis.md","w") as f:
    f.write(f"""API Summary:
Total endpoints: {total_endpoints}
HTTP methods: {dict(methods)}
Auth methods: {list(auth_methods)}
With responses: {with_resp}
Missing responses: {without_resp}
Response codes: {sorted(resp_codes)}
Coverage: {round(coverage,2)}%""")

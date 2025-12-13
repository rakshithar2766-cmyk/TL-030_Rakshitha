import logging, yaml, json, os
from collections import Counter
from datetime import datetime

logger = logging.getLogger("API_Logger")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter(
    '{"timestamp":"%(asctime)s",'
    '"level":"%(levelname)s",'
    '"component":"%(component)s",'
    '"message":"%(message)s",'
    '"exception_code":"%(exception_code)s"}'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

def log_info(component, msg):
    logger.info(msg, extra={"component": component, "exception_code": "NA"})

def log_error(component, msg, code):
    logger.error(msg, extra={"component": component, "exception_code": code})

def load_yaml(file):
    if not os.path.exists(file):
        log_error("Parser", "YAML file not found", "YAML404")
        return None
    try:
        data = yaml.safe_load(open(file))
        log_info("Parser", "YAML file loaded successfully")
        return data
    except yaml.YAMLError:
        log_error("Parser", "YAML parsing failure", "YAML500")
        return None


def validate_metadata(data):
    if not data or "paths" not in data:
        log_error("Client", "Missing or invalid metadata", "META400")
        return False
    log_info("Client", "Metadata validated successfully")
    return True


def generate_summary(files):
    total, with_resp, without_resp = 0, 0, 0
    methods = Counter()
    auth = set()
    resp_codes = set()

    for f in files:
        data = load_yaml(f)
        if not data or not validate_metadata(data):
            continue

        auth.update(data.get("components", {}).get("securitySchemes", {}).keys())

        for path, mths in data["paths"].items():
            for m, d in mths.items():
                total += 1
                methods[m.upper()] += 1
                responses = d.get("responses", {})
                if responses:
                    with_resp += 1
                    resp_codes.update(responses.keys())
                else:
                    without_resp += 1

    coverage = (with_resp / total * 100) if total else 0

    summary = {
        "total_endpoints": total,
        "http_method_distribution": dict(methods),
        "authentication_methods": list(auth),
        "endpoints_with_responses": with_resp,
        "endpoints_missing_responses": without_resp,
        "response_codes_encountered": sorted(resp_codes),
        "coverage_percentage": round(coverage, 2),
        "generated_at": str(datetime.now())
    }

    json.dump(summary, open("summary.json", "w"), indent=2)
    log_info("Summary", "Summary generation completed")

    with open("README.md", "a") as f:
        f.write(
            f"\n\n## API Summary\n"
            f"- Total endpoints: {total}\n"
            f"- HTTP methods: {dict(methods)}\n"
            f"- Auth methods: {list(auth)}\n"
            f"- Coverage: {round(coverage,2)}%\n"
        )

if __name__ == "__main__":
    api_files = ["api1.yaml","api2.yaml","api3.yaml","api4.yaml","api5.yaml"]
    generate_summary(api_files)



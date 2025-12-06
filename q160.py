import logging
logging.basicConfig( filename="system.log",level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s")

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console.setFormatter(formatter)

logging.getLogger().addHandler(console)

try:
    raise ValueError("Example failure")
except Exception as e:
    logging.error(f"Error occurred: {e}")
    console = logging.StreamHandler()
console.setLevel(logging.INFO)



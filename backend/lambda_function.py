import json

from roboteacher.tasks import delete_data, fetch_data, scrap_data, seed_data


def lambda_handler(event, context) -> dict:
    functions = {
        "scrap_data": scrap_data,
        "fetch_data": fetch_data,
    }

    task = event.get("task", "scrap_data")
    print("task:", task)
    return functions[task]()


if __name__ == "__main__":
    print(json.dumps(scrap_data(), indent=2))
    seed_data()
    print(json.dumps(fetch_data(), indent=2, ensure_ascii=False))
    delete_data()

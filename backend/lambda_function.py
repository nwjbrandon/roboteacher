from roboteacher.tasks import fetch_data, scrap_data


def lambda_handler(event, context) -> dict:
    functions = {
        "scrap_data": scrap_data,
        "fetch_data": fetch_data,
    }

    task = event.get("task", "scrap_data")
    print("task:", task)
    return functions[task]()

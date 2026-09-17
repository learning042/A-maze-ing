def is_readable_line(line: str) -> bool:
    line = line.strip()
    if line == "":
        return False
    elif line.count("=") != 1:
        return False
    elif "=" in (line[0], line[-1]):
        return False
    elif line[0] == "#":
        return False
    return True


def find_duplicate(keys: list[str]) -> str | None:
    seen = set()
    for key in keys:
        if key in seen:
            return key
        else:
            seen.add(key)
    return None


def build_config_dict() -> dict[str, str | int | tuple[int, int]]:
    with open("config.txt", "r") as file:
        buffer = [line for line in file.read().split("\n") if is_readable_line(line)]
    keys = [key.split("=")[0] for key in buffer]
    values = [value.split("=")[1] for value in buffer]
    duplicate = find_duplicate(keys)
    if duplicate is not None:
        raise Exception(f"Duplicate key {duplicate} in file 'config.txt'")
    config = {key: value for (key, value) in zip(keys, values)}
    built_config: dict[str, str | int | tuple[int, int]] = {}
    for key in config.keys():
        if key == "OUTPUT_FILE":
            continue
        elif key == "PERFECT":
            if config[key].title() not in ("True", "False"):
                raise ValueError("PERFECT should be either 'True' or 'False'")
            else:
                built_config[key] = bool(config[key])
        elif key in ("WIDTH", "HEIGHT", "SEED"):
            built_config[key] = int(config[key])
        elif key in ("ENTRY", "EXIT"):
            value = tuple(map(int, config[key].split(",")))
            if len(value) != 2:
                raise ValueError(
                    f"Incorrect format of dictionary[{key}] value",
                    " it should be 'int,int' format"
                    )
            built_config[key] = value
        else:
            raise Exception(f"Invalid key: '{key}' in file 'config.txt'.")
    if len(config) != 7:
        raise ValueError(
            "Invalid dictionary size.",
            " It must have something extra or something missing.")
    return built_config


if __name__ == "__main__":
    config = build_config_dict()
    print(config)

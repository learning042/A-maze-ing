def is_valid_line(line: str) -> bool:
    line = line.strip()
    if line == "":
        return False
    elif line[0] == "#":
        return False
    elif line[0] == " ":
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
        buffer = [line for line in file.read().split("\n") if is_valid_line(line)]
    keys = [key.split("=")[0] for key in buffer]
    values = [value.split("=")[1] for value in buffer]
    duplicate = find_duplicate(keys)
    if duplicate != None:
        raise Exception(f"Duplicate key {duplicate} in file 'config.txt'")
    config = {key: value for (key, value) in zip(keys, values)}
    for key in config.keys():
        if key == "OUTPUT_FILE":
            continue
        elif key == "PERFECT":
            if config[key].title() not in ("True", "False"):
                raise ValueError("PERFECT should be either 'True' or 'False'")
            else:
                config[key] = bool(config[key])
        elif key in ("WIDTH", "HEIGHT", "SEED"):
            config[key] = int(config[key])
        elif key in ("ENTRY", "EXIT"):
            value = tuple(map(int, config[key].split(",")))
            if len(value) != 2:
                raise ValueError(f"Incorrect format of dictionary[{key}] value, it should be 'int,int' format")
            config[key] = value 
        else:
            raise Exception(f"Invalid key: '{key}' in file 'config.txt'.")
    if len(config) != 7:
        raise Exception("Invalid dictionary size. It must have something extra or something missing.")
    return config



if __name__ == "__main__":
    config = build_config_dict()
    print(config)

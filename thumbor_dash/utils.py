from datetime import datetime

def dashauthParametersToJson(params):
    temp = params.split(":")

    result = {}

    for p in temp:
        key_value_pair = p.split("(")
        key = key_value_pair[0]

        temp_value = key_value_pair[1]
        value = temp_value[0:- 1]
        real_value = int(value) if key == "updatedAt" else value

        result[key] = real_value

    return result


def datetimeToMillisecondsSinceEpoch(dt):
    epoch = datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0

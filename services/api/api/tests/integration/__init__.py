def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def frmt_msg_invalid_status_code(expected, returned):
    return "invalid status code...\n" \
        "\texpected: {}\n" \
        "\treturned: {}".format(expected, returned)


def frmt_msg_invalid_response_body(expected, returned):
    return "invalid response body...\n" \
        "\texpected: {}\n" \
        "\treturned: {}".format(expected, returned)

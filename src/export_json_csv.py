import csv
import getopt
import io
import json
import sys

quote_char = '"'
delimiter = ','


def main(param):
    args = validate_cli_arguments(param)
    json_file_name = args[0]
    data = load_json_data(json_file_name)
    field_names = get_field_names(data)

    write_csv(data, field_names, json_file_name)


def write_csv(data, field_names, json_file_name):
    proxy = io.StringIO()
    writer = csv.DictWriter(proxy, fieldnames=field_names, delimiter=delimiter,
                            quotechar=quote_char, quoting=csv.QUOTE_NONNUMERIC)
    writer.writeheader()
    for item in data:
        result = dict.fromkeys(item)
        for key in item:
            result[key] = list(item[key].values())[0]
        writer.writerow(result)
    mem = io.BytesIO()
    mem.write(proxy.getvalue().encode('utf-8'))
    mem.seek(0)
    proxy.close()
    if mem:
        mem.seek(0)
        with open(json_file_name + ".csv", mode='wb') as persist_file:
            persist_file.write(mem.read())
            mem.close()
            persist_file.close()
            print(persist_file.name + ' OK')
    else:
        print(f"There's no data for user")


def get_field_names(data):
    field_names = list(set().union(*(item.keys() for item in data)))
    return field_names


def load_json_data(json_file_name):
    with open(json_file_name) as json_file:
        data = json.load(json_file)
    data = data['Items']
    return data


def validate_cli_arguments(param):
    try:
        opts, args = getopt.getopt(param, "f", ["file="])
        if not opts:
            raise getopt.GetoptError('Bad arguments.')
    except getopt.GetoptError:
        print('usage: main.py -f <json file>')
        sys.exit(2)
    return args


if __name__ == "__main__":
    main(sys.argv[1:])

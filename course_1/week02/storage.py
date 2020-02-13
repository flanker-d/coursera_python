import os
import tempfile
import argparse
import json

storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
#storage_path = 'storage.data'

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("--key", help="key name")
  parser.add_argument("--val", help="value")
  args = parser.parse_args()

  key = None
  value = None

  if args.key:
    key = args.key

  if args.val:
    value = args.val

  return (key, value)

def read_key(key):

  if os.path.isfile(storage_path):
    with open(storage_path, 'r') as f:
      json_obj = json.load(f)
      if key in json_obj:
        values_list = json_obj[key]
        result = ", ".join(map(str, values_list))
        print(result)
      else:
        print("None")
  else:
    print("None")

def write_value(key, value):
  if os.path.isfile(storage_path):
    json_obj = {}
    with open(storage_path, "r") as f:
      json_obj = json.load(f)

    with open(storage_path, "w") as f:
      value_list = []
      if key in json_obj:
        value_list = json_obj[key]
        value_list.append(value)
      else:
        value_list = [value]

      json_obj[key] = value_list
      json.dump(json_obj, f)
  else:
    with open(storage_path, "w") as f:
      json_obj = {}
      value_list = [value]
      json_obj[key] = value_list
      json.dump(json_obj, f)

key, value = parse_args()

if key != None and value == None:
  read_key(key)
elif key != None and value != None:
  write_value(key, value)
else:
  print("None")
import os
import re
import sys
import json
import inspect
import datetime
import traceback
from functools import wraps


class CommonMethod:
    outputFormat = re.compile(r"([A-Z])")
    inputFormat = re.compile(r"_([a-z])")

    @staticmethod
    def validate_datetime_format(val, format):
        try:
            datetime.datetime.strptime(val, format)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_time(val, format):
        try:
            datetime.datetime.strptime(val, format)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_datetime(start, end, startformat, endformat):
        result = False
        try:
            startdate = datetime.datetime.strptime(start, startformat)
            enddate = datetime.datetime.strptime(end, endformat)
            if enddate > startdate:
                result = True
        except ValueError:
            result = False
        return result

    def convert_input_format(self, name):
        return self.outputFormat.sub(lambda x: "_" + x.group(1).lower(), name)

    def convert_output_format(self, name):
        return self.inputFormat.sub(lambda x: x.group(1).upper(), name)

    def convert_json(self, obj, convert):
        if isinstance(obj, list):
            new_list = []
            for o in obj:
                new_json = {}
                for k, v in o.items():
                    v = (
                        v.isoformat().replace("+05:30", "Z")
                        if isinstance(v, datetime.datetime)
                        else v
                    )
                    new_json[convert(k)] = (
                        self.convert_json(v, convert) if isinstance(v, dict) else v
                    )
                new_list.append(new_json)
            return new_list
        else:
            new_json = {}
            for k, v in obj.items():
                v1 = v[0] if isinstance(v, list) and v else v
                v = (
                    v.isoformat().replace("+05:30", "Z")
                    if isinstance(v, datetime.datetime)
                    else v
                )
                new_json[convert(k)] = (
                    self.convertJson(v, convert)
                    if isinstance(v1, dict) or isinstance(v1, list)
                    else v
                )
            return new_json

    def output_json(self, obj):
        return self.convert_json(obj, self.convert_output_format)

    def input_json(self, obj):
        return self.convert_json(obj, self.convert_input_format)

    def without_verbose(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (
            RuntimeError,
            TypeError,
            NameError,
            ImportError,
            IndexError,
            KeyError,
        ) as e:
            return outputJson({"message": str(e), "code": 422})
        except Exception as e:
            return outputJson({"message": str(e), "code": 422})

    def with_verbose(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            exec_type, exec_obj, exec_tb = sys.exc_info()
            ln = traceback.extract_tb(exec_tb)[-1]
            line = str(ln).split(", ")[-1].replace(">", "")
            message = exec_obj.with_traceback(exec_tb)
            file = os.path.abspath(inspect.getfile(func))

            error = {
                "error": str(exec_type),
                "code": 422,
                "file": file,
                "func": func.__name__,
                "location": line,
                "message": repr(message),
                "args": args,
                "kwargs": kwargs,
            }
            return {"message": str(error), "code": 422}

    def try_except(self, verbose=False):
        def inner(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                mappings = {
                    True: self.with_verbose,
                    False: self.without_verbose,
                }
                return mappings.get(verbose, False)(func, *args, **kwargs)

            return wrapper

        return inner


def sort_queryset(queryset, key):
    SORT_FIELDS = {
        "id": "id",
        "name": "name",
        "created_at": "created_at",
        "updated_at": "-updated_at",
    }
    sort_field = SORT_FIELDS.get(key, "created_at")
    queryset = queryset.order_by(sort_field)
    return queryset


common = CommonMethod()
output_json = common.output_json
input_json = common.input_json
try_except = common.try_except

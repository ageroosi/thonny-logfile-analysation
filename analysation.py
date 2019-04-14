import json
from collections import defaultdict
import dateutil.parser

# Author of the function is Heidi Meier

# Function for understanding if the given key and the right value exist in the json element
# If third argument is False, then the value has to be present in the right value
# If third argument is True, then the value has to equal the right value
def in_json(element, key, value, exact=True):
    if key not in element:
        return False
    if exact:
        return element[key] == value
    else:
        return element[key].find(value) != -1

# Author of the function is Heidi Meier

# Function for understanding whether the code running results in error
# If json element text is ">>> ", then the element before that contains tag "error" or "stderr", if resulted in error
def results_in_error(data, i):
    while not in_json(data[i+1], "text", ">>> "):
        i += 1
    return in_json(data[i], "text_widget_class", "ShellText") and (in_json(data[i], "tags", "error", False) or in_json(data[i], "tags", "stderr", False))

# Function for log file analysation
def analysation(filename, pasted_text_size):
    # Reading logfile data
    logifail = open(filename)
    data = json.load(logifail)  # sõnastike listina
    logifail.close()

    # Dictionary for keeping logfile information
    analysation_dict = defaultdict(list)

    # Adding starting and finishing time
    analysation_dict['start_time'].append(dateutil.parser.parse(data[0]["time"]))
    analysation_dict['end_time'].append(dateutil.parser.parse(data[-1]["time"]))

    for i in range(len(data)):
        # Logfile json element
        element = data[i]
        # Finding running information
        if in_json(element, "sequence", "ShellCommand") and in_json(element, "command_text", "%Run", False):
            analysation_dict['running'].append(dateutil.parser.parse(element["time"]))
            analysation_dict['running_results_in_error'].append(results_in_error(data, i))
        # Finding error information
        elif in_json(element, "sequence", "TextInsert") and in_json(element, "text", "Error", False):
            txt = element['text']
            analysation_dict['errors'].append(txt)
            analysation_dict['error_time'].append(dateutil.parser.parse(element["time"]))
            analysation_dict['error_type'].append(txt.split(":", 1)[0])
            analysation_dict['error_message'].append(txt.split(": ", 1)[1].strip('\n'))
        # Finding information about savings
        elif in_json(element, "sequence", "Save", False):
            analysation_dict['saving_time'].append(dateutil.parser.parse(element["time"]))
        # Fiding information about pasted texts
        elif in_json(element, "sequence", "<<Paste>>"):
            if len(data[i - 1]['text']) >= pasted_text_size:
                analysation_dict['pasted_text'].append(data[i-1]['text'])
                analysation_dict['pasted_text_time'].append(dateutil.parser.parse(data[i - 1]["time"]))
    return analysation_dict

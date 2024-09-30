import re
import numpy as np


def AlphaGrade2Percentage(mark):
    """
    convert grade A-U to corresponding percentage
    """
    if mark.upper() in ["A", "A*", "A+", "A-"]:
        return 95
    elif mark.upper() == "B":
        return 85
    elif mark.upper() == "C":
        return 75
    elif mark.upper() == "D":
        return 65
    elif mark.upper() == "E":
        return 55
    elif mark.upper() == "F":
        return 45
    elif mark.upper() == "U":
        return 25
    return 0


def calculate_percentage(mark, out_of):
    """
    calculate the percentage from 0-100 using string mark & out of
    as long as the input string (mark, out of score) is valid, else returns 0
    """
    try:
        # Some teacher would add "Out of" string before the real out-of mark, hence delete them
        out_of = out_of.replace("Out of", "").strip()
        # Some teacher would add extra string after real numeric mark, hence only match numeric part
        match = re.match(r'^(\d+)', mark)
        if match:
            # convert to float & calculate percentage
            mark_float = float(match.group(1))
            perc = int(mark_float / float(out_of) * 100)
            # if the percentage is invalid
            if perc > 100 or perc < 0:
                # check if mark could be a valid percentage
                if 100 >= mark_float >= 0:
                    return mark_float
                # if no, just return 100 as default
                return 100
            else:
                # percentage is valid
                return perc
        else:
            raise ValueError
    except ValueError:
        # Try to match Grade A-U and convert to corresponding percentage
        perc = AlphaGrade2Percentage(mark)
        if perc == 0:
            print("Value Error:", mark, "out of", out_of)
        return perc
    # Other error cases:
    except ZeroDivisionError:
        print("Division by 0:", mark, "out of", out_of)
        return -1
    except TypeError:
        print("Type Error:", mark, "out of", out_of)
        return 0
    except Exception as e:
        print(f"{e}:", mark, "out of", out_of)
        return 0


def prevent_duplicates(input_list):
    """
    Prevents duplicates in the input list by adding a suffix (2), (3), etc.
    for repeated values.
    """
    seen = {}  # Dictionary to track the occurrences of each value
    result = []  # List to store the unique values with suffixes if necessary

    for item in input_list:
        if item not in seen:
            # First occurrence, add to result as is
            seen[item] = 1
            result.append(item)
        else:
            # Handle duplicates
            seen[item] += 1
            new_item = f"{item}({seen[item]})"
            result.append(new_item)

    return result


def calculate_quadrants(data):
    """
    calculate min, max, 1st and 3nd quadrants
    from a series of data.
    """
    if len(data) < 1:
        return [0, 0, 0, 0]
    lowest = np.min(data)
    highest = np.max(data)
    first_quartile = np.percentile(data, 25)
    third_quartile = np.percentile(data, 75)
    return [float(first_quartile), float(third_quartile), float(lowest), float(highest)]


def calculate_average(data):
    """
    calculate average from a series of data.
    """
    average = np.average(data)
    return round(float(average), 2)


def get_assessment_percentages(assessments):
    """
    Get headings, score percentages and average percentages from a list of assessments.
    """
    heads = prevent_duplicates([i["title"] for i in assessments])
    value = [calculate_percentage(i["mark"], i["out_of"]) for i in assessments]
    average = [calculate_percentage(i["average"], i["out_of"]) for i in assessments]
    return heads, value, average

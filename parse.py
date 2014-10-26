"""
These dictionaries define the relationship between the column header as
it will appear in the student data and course data spreadsheets and the
parameters to construct these two objects.
"""
student_headers = {
    "ID": "student_id",
    "First Name": "first_name",
    "Last Name": "last_name",
    "Submitted Date": "time_submitted",
    "First Year Seminar DDB 1": "pref_one",
    "First Year Seminar DDB 2": "pref_two",
    "First Year Seminar DDB 3": "pref_three"
}

course_headers = {
    "Course Name": "course_name",
    "Size": "seats"
}

# Wrapper around get_header_indices that uses the values defined in 
# student_headers. See get_header_indices.
def get_student_headers(sheet):
    return get_header_indices(sheet, student_headers)

# Wrapper around get_header_indices that uses the values defined in 
# course_headers. See get_header_indices.
def get_course_headers(sheet):
    return get_header_indices(sheet, course_headers)

"""
Identifies the column numbers in a sheet where columns have known
header values.

sheet  xlrd.Sheet  the sheet to use in identifying headers
labels  Dict  a dictionary with keys corresponding to the headers as
  they will appear in the spreadsheet, and values corresponding to the
  desired key value in the return dict

Returns a dict of the format:
  {
    "name": n,
    ...
  }
where the keys are the names of the properties and the values are the
corresponding column numbers.
"""
def get_header_indices(sheet, labels):
    header_indices = {}
    for col in range(sheet.ncols):
        header = sheet.cell_value(0, col)
        try:
            header_key = labels[header]
            header_indices[header_key] = col
        except KeyError:
            continue

    return header_indices

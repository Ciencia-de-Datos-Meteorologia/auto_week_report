import google_tools

drive_service = google_tools.get_drive_service()

files = google_tools.list_files('1gOzvoBpXS1hzAwIE3ihJEvoBXT9lj45b', drive_service)
date_dir = google_tools.find_file_by_path(
    '2024-08-19/gasamayoa', drive_service, '1gOzvoBpXS1hzAwIE3ihJEvoBXT9lj45b')

print(date_dir)
print(files)

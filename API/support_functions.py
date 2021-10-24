import random
from werkzeug.utils import secure_filename


def create_code(start_number, stop_number):
    return str(random.randint(start_number, stop_number))


def save_files(request):
    data_info = request
    data_files = request.files.lists()
    print(request.files)
    # print(data_files)
    for data in data_files:
        print(data)
        user_code = data[0]
        print(user_code)
        for items in data[1]:
            file_name = secure_filename(items.filename)
            items.save(f"./users_files/{file_name}")
            yield f"./users_files/{file_name}"

import random
import string
import datetime


def generate_api_key(username):
    chars = string.ascii_letters + string.digits
    random_string = "".join(random.choice(chars) for _ in range(10))
    created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
    created_at_list = list(str(created_at))
    random.shuffle(created_at_list)
    random_created_at = "".join(created_at_list)
    result = f"{username}{random_string}{random_created_at}"
    result_list = list(result)
    random.shuffle(result_list)
    return "".join(result_list)

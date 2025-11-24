import uuid

def generate_new_receipt():
    return "R-" + uuid.uuid4().hex[:10].upper()

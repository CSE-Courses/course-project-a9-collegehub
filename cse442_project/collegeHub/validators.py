import os

def validate_pdf(value):
    file_extension = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.pdf']
    if file_extension in valid_extensions:
        return True
    return False

def validate_image(value):
    file_extension = os.path.splitext(value.name)[1].lower()
    print(file_extension)
    valid_extensions = ['.jpg', '.jpeg', '.jpe' '.jif', '.jfif', '.jfi', '.png', '.webp']
    if file_extension in valid_extensions:
        return True
    return False
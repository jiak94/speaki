import os


def test_azure_blob(azure_storage_service):
    f = open("./hello_world.txt", "w")
    f.write("Hello World!")
    f.close()

    file = os.path.join("./", "hello_world.txt")
    azure_storage_service.upload_file(file)

    os.remove(file)

import boto3
import os


session = boto3.Session()
s3 = session.client(service_name='s3')


def read_files(bucket='antsib-bucket'):
    try:
        print("Files in bucket:")
        files_list = s3.list_objects(Bucket=bucket)['Contents']
    except Exception as e:
        print(e)
        return False
    else:
        for key in s3.list_objects(Bucket=bucket)['Contents']:
            print(key['Key'])
        print("\n")
        return True


def upload_file(file_name, bucket='antsib-bucket'):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    file_dir = "upload_files"
    file_dir = os.path.join(this_dir, file_dir)
    file_path = os.path.join(file_dir, file_name)

    try:
        with open(file_path, 'rb') as f:
            s3.upload_fileobj(f, bucket, file_name)
    except Exception as e:
        print(e)
        return False
    return True


def download_file(file_name, bucket='antsib-bucket'):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    file_dir = "download_files"
    file_dir = os.path.join(this_dir, file_dir)

    try:
        with open(os.path.join(file_dir, file_name), 'wb') as f:
            s3.download_fileobj(bucket, file_name, f)
        if os.path.exists(os.path.join(file_dir, file_name)):
            print(f"File {file_name} has been downloaded!")
    except Exception as e:
        print(e)
        return False
    return True


def delete_file(file_name, bucket='antsib-bucket'):
    try:
        response = s3.delete_object(Bucket=bucket, Key=file_name)
    except Exception as e:
        print(e)
        return False
    return True


if __name__ == '__main__':
    read_files()
    upload_file("config.py")
    read_files()
    delete_file("config.py")
    read_files()
    download_file("flask_server.py")
    
from _event import _event as _event_

"""
pip install poetry
poetry init

poetry add pyyaml
poetry add boto3
poetry add pandas
poetry add pygithub

pip install pyyaml
pip install boto3
pip install pandas
pip install pygithub

"""
from task.s3 import add_s3_bucket
from task.s3 import upload_file_s3
from task.s3 import create_presign_url


def main():
    # add_s3_bucket.add_s3_bucket("pg-share-out-001")
    # upload_file_s3.s3_upload_file("/Users/jianhuang/Downloads/jianhuang_picture.jpg", "s3://pg-share-out-001")

    # _event_.order_of_events()

    print(create_presign_url.s3_upload_file("s3://pg-share-out-001/jianhuang_picture.jpg", expiration=604800))


if __name__ == '__main__':
    main()

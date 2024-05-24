from _connect import _connect as _connect_


def example():
    _object_s3 = _connect_.get_object("awss3")
    print(_object_s3.create_presigned_url("s3://pg-share-out-001/aws.jpg", expiration=604800))


if __name__ == '__main__':
    example()

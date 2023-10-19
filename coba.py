import sqz

def test_copy_data():
    compressed_file = "LEVEL1.SQZ"
    output_file = "LEVEL1.bin"
    bytes_copied = sqz.decompress(compressed_file, output_file)

    # with open('test_write.txt', 'r') as f:
    #     content_copied = f.read()

    # assert content_copied == content_to_copy


if __name__ == '__main__':
    test_copy_data()
    print(sqz.__doc__)
    # print(sqz.sqz.__doc__)
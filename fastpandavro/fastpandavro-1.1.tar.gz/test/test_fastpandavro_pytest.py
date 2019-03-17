import os

from fastpandavro import pandas_to_avro, avro_to_pandas


def test_faastpandavro():
    df = avro_to_pandas(fname="c:/Users/099391/Documents/fastpandavro/test/sample.avro")
    assert df.shape[0] > 0
    fname = "sample_output.avro"
    pandas_to_avro(df, fname, schema_file="c:/Users/099391/Documents/fastpandavro/test/sample.avsc")
    assert os.path.isfile(fname)
    if os.path.isfile("sample_output.avro"):
        os.remove("sample_output.avro")

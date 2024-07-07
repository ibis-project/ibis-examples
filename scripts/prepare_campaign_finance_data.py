from pathlib import Path
from urllib.request import urlretrieve
from zipfile import ZipFile

import ibis

# Download and unzip the 2018 individual contributions data
url = (
    "https://cg-519a459a-0ea3-42c2-b7bc-fa1143481f74.s3-us-gov-west-1."
    "amazonaws.com/bulk-downloads/2018/indiv18.zip"
)

root_dir = Path(__file__).resolve().parent.parent
data_dir = root_dir.joinpath("data")
data_dir.mkdir(exist_ok=True)

zip_path = data_dir.joinpath("indiv18.zip")
csv_path = data_dir.joinpath("itcont.txt")
parquet_path = data_dir.joinpath("itcont.parquet")

if not zip_path.exists():
    print("Downloading indiv18.zip...")
    urlretrieve(url, zip_path)
else:
    print("indiv18.zip already downloaded")

if not csv_path.exists():
    print("Extracting itcont.txt...")
    with ZipFile(zip_path) as zip_file:
        zip_file.extract("itcont.txt", path=data_dir)
else:
    print("itcont.txt already extracted")

if not parquet_path.exists():
    print("Generating itcont.parquet...")
    # Read in the CSV
    # The CSV doesn't have a header, we need to manually add titles
    t = ibis.read_csv(
        csv_path,
        header=False,
        names=[
            "CMTE_ID",
            "AMNDT_IND",
            "RPT_TP",
            "TRANSACTION_PGI",
            "IMAGE_NUM",
            "TRANSACTION_TP",
            "ENTITY_TP",
            "NAME",
            "CITY",
            "STATE",
            "ZIP_CODE",
            "EMPLOYER",
            "OCCUPATION",
            "TRANSACTION_DT",
            "TRANSACTION_AMT",
            "OTHER_ID",
            "TRAN_ID",
            "FILE_NUM",
            "MEMO_CD",
            "MEMO_TEXT",
            "SUB_ID",
        ],
    )

    # For the analysis, we're only going to use a few of the columns. To save
    # bandwidth, lets select out only the columns we'll be using.
    columns = [
        "CMTE_ID",
        "TRANSACTION_PGI",
        "ENTITY_TP",
        "CITY",
        "STATE",
        "TRANSACTION_DT",
        "TRANSACTION_AMT",
    ]
    t = t[columns]

    # Write out a parquet file
    t.to_parquet(parquet_path, compression="zstd")
else:
    print("itcont.parquet already exists")

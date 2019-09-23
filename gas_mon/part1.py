import json
import logging
import boto3

logging.basicConfig(filename='GasMon.log', filemode='w', level=logging.DEBUG)  # configures the log

s3 = boto3.resource("s3")


class Location:
    def __init__(self, x, y, i_d):
        self.x = x
        self.y = y
        self.id = i_d


def download_locations_file():
    try:
        with open("config.json", "r") as file:
            logging.info("Collecting information for AWS configuration.")
            contents = json.load(file)
            arn = contents["ARN"]
            bucket = contents["Bucket"]
            key = contents["Key"]
            filename = contents["Filename"]
            logging.info("Information collected.")
    except FileNotFoundError:
        print("The file config.json could not be found.")
        logging.info("The file config.json could not be found.")

    logging.info("Downloading file.")
    s3.meta.client.download_file(bucket, key, filename)
    logging.info("File successfully downloaded. Saved as: " + filename)
    return filename


def read_json_of_locations():
    filename = download_locations_file()
    logging.info(filename + " opened in read mode.")
    with open(filename, "r") as file:
        locations = json.load(file)
        for raw_location in locations:
            loc = Location(raw_location["x"], raw_location["y"], raw_location["id"])
            print(loc.x, loc.y, loc.id)
    logging.info("File read. x and y coordinates and id's obtained.")


download_locations_file()
read_json_of_locations()

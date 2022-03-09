from quixstreaming import StreamWriter
from datetime import datetime
import time
import pandas as pd


class Functions:

    # should the main loop run?
    run = True

    def __init__(self, stream_writer: StreamWriter):
        self.stream_writer = stream_writer

    def write_data(self):

        df = pd.read_csv("currency_data.csv")
        headers = list(df)

        while self.run:
            for index, row in df.iterrows():

                # make a row to write to the stream
                data_frame_row = pd.DataFrame()
                data_frame_row["time"] = [datetime.utcnow()]
                for header in headers:
                    value = row[header]
                    data_frame_row[header] = [value]

                self.stream_writer.parameters.buffer.write(data_frame_row)
                time.sleep(0.1)

        print("Closing stream")

        # Stream can be infinitely long or have start and end.
        # If you send data into closed stream, it is automatically opened again.
        self.stream_writer.close()

    def stop_loop(self):
        self.run = False

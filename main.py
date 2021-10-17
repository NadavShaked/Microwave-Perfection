#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from tensorflow import keras
import matplotlib.image as mpimg
import cv2
import numpy as np

prediction_to_label = [('soup', lambda x: 0 if x == 0 else 0.25 * x + 3),
                       ('bread', lambda x: 0 if x == 0 else 0.45 * x + 7),
                       ('pasta', lambda x: 0 if x == 0 else 0.4 * x + 12),
                       ('rise', lambda x: 0 if x == 0 else 0.4 * x + 12), ('vegetable', lambda x: 0)]


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        print()
        content_length = int(self.headers['content-length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself

        with open("imageToSave.jpg", "wb") as fh:
            bytesData = bytes(post_data)
            fh.write(base64.decodebytes(bytesData))

        image = mpimg.imread('imageToSave.jpg')
        after_corp_img = cv2.resize(image, (120, 120))

        predict_arr = model.predict(np.array([after_corp_img, ]))
        print(predict_arr)
        predict_index = np.argmax(predict_arr)
        predict = prediction_to_label[predict_index]
        numOfSeconds = predict[1](int(self.headers['weight']))
        mins = int(numOfSeconds / 60)
        seconds = int(numOfSeconds % 60)
        time = f'00:{"0" + str(mins) if mins < 10 else str(mins)}:{"0" + str(seconds) if seconds < 10 else str(seconds)}'

        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data.decode('utf-8'))
        print(predict[0], time)
        self._set_response()
        self.wfile.write(time.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig()
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    from sys import argv

    model = keras.models.load_model('Model')

    if len(argv) == 2:
        run(int(argv[1]))
    else:
        run()

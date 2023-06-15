import tornado.web
import tornado.ioloop
import tornado.httpclient

import torch
from matplotlib import pyplot as plt
import numpy as np
import cv2
import json as json
from json import loads

import uuid
import os
import time

from variables import *
from detecting import *

class uploadHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods',
                        ' PUT, DELETE, OPTIONS')

    def options(self):
        # no body
        self.set_status(204)
        self.finish()

    def post(self):
        print(self.request);
        files = self.request.files["image"]
        # self.write(f"<html><body><p>{csrf}</p></body></html>")
        for f in files:
            fh = open(f"img/{f.filename}", "wb")
            fh.write(f.body)
            fh.close()
        print(f.filename)
        image = f.body
        np_img = np.array(image)
        results = modelEenheden(f"img/{f.filename}", size=1280)
        array = results.pred[0].cpu().numpy()
        if array.size == 0:
            # os.remove(f"img/{f.filename}")
            self.write("no detection")
            print("no detection")
        else:
            detections = detect(array)
            json_det = JSONDetections(detections)
            self.write(json_det)
            print(json_det)
            # os.remove(f"img/{f.filename}")

class uploadOPHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods',
                        ' PUT, DELETE, OPTIONS')

    def options(self):
        # no body
        self.set_status(204)
        self.finish()

    def post(self):
        print(self.request);
        files = self.request.files["image"]
        # self.write(f"<html><body><p>{csrf}</p></body></html>")
        for f in files:
            fh = open(f"img/{f.filename}", "wb")
            fh.write(f.body)
            fh.close()
        print(f.filename)
        image = f.body
        np_img = np.array(image)
        results = modelOppervlakte(f"img/{f.filename}", size=1280)
        array = results.pred[0].cpu().numpy()
        if array.size == 0:
            # os.remove(f"img/{f.filename}")
            self.write("no detection")
            print("no detection")
        else:
            detections = detectOP(array)
            json_det = JSONOPDetections(detections)
            self.write(json_det)
            print(json_det)
            # os.remove(f"img/{f.filename}")

if(__name__ == "__main__"):

    app = tornado.web.Application([
        ("/", uploadHandler),
        ("/OP", uploadOPHandler),
        ("/img/(.*)", tornado.web.StaticFileHandler, {"path" : "img"})
    ])
    app.listen(8080)
    print("Listening on port 8080")
    modelEenheden = torch.hub.load('ultralytics/yolov5', 'custom', path='Model/best_eenheden.pt')
    modelOppervlakte = torch.hub.load('ultralytics/yolov5', 'custom', path='Model/best_oppervlakte.pt')
    print("Model loaded")
    tornado.ioloop.IOLoop.instance().start()

import cv2
import logging
import argparse
import utils.datasets as datasets
from utils.utils import *
from utils.log import logger
from utils.timer import Timer
from utils.parse_config import parse_model_cfg
from track import eval_seq
from flask import Flask, render_template, jsonify,request
import datetime
import random

app = Flask(__name__)

class opt:
    cfg = 'cfg/yolov3_1088x608.cfg'
    weights = 'weights/jde.1088x608.uncertainty.pt'
    iou_thres = 0.5
    conf_thres = 0.5
    nms_thres = 0.4
    min_box_area = 200
    track_buffer = 30
    output_root = 'results'

@app.route('/')
def index():
    # Get newest file path
    return render_template("index.html")


@app.route('/api/track')
def track():
    # set saving dir
    print('================= start =================')
    result_root = opt.output_root if opt.output_root!='' else '.'
    mkdir_if_missing(result_root)

    # set configuration
    cfg_dict = parse_model_cfg(opt.cfg)
    opt.img_size = [int(cfg_dict[0]['width']), int(cfg_dict[0]['height'])]

    logger.info('Starting tracking...')
    # use camera to track
    dataloader = datasets.LoadCamera(img_size=opt.img_size)
    #dataloader = datasets.LoadVideo("./static/data/video01.mp4")
    result_filename = os.path.join(result_root, 'results.txt')

    try:
        # start tracking
        frame_id, timer.average_time, timer.calls, online_ids = eval_seq(opt, dataloader, 'mot', result_filename,
                                                                    save_dir=result_root, show_image=True)
        
    except Exception as e:
        logger.info(e)

    

@app.route('/api/test')
def test_page():
    data = [random.randrange(1, 10, 1) for i in range(7)]
    data.insert(0,'All')
    print(data)
    #return str(datetime.datetime.now())  # 示範用
    return jsonify(data)

@app.route('/get_select_id',methods=['GET','POST'])
def get_select_id():
    print("---get_select_id")
    if request.method == 'POST':
        get_data = request.json['id']
        print(get_data)
    
        return jsonify(get_data) 
    else: 
        return render_template('index.html')

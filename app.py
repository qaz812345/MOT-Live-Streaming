
import cv2
import logging
import argparse
import utils.datasets as datasets
from utils.utils import *
from utils.log import logger
from utils.timer import Timer
from utils.parse_config import parse_model_cfg
from track import eval_seq, get_online_ids
from flask import Flask, render_template, jsonify,request
import datetime
import random

app = Flask(__name__)
get_data = 0

class opt:
    cfg = 'cfg/yolov3_1088x608.cfg'
    weights = 'weights/jde.1088x608.uncertainty.pt'
    iou_thres = 0.5
    conf_thres = 0.5
    nms_thres = 0.4
    min_box_area = 200
    track_buffer = 30
    output_root = 'static/data'



@app.route('/')
def index():
    # Get newest file path
    return render_template('index.html',name="")


@app.route('/api/track',methods=['GET'])
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
    #dataloader = datasets.LoadCamera(img_size=opt.img_size)
    dataloader = datasets.LoadVideo("./static/data/video01.mp4")
    result_filename = os.path.join(result_root, 'results.txt')

    try:
        # start tracking
        eval_seq(opt, dataloader, 'mot', result_filename,
                save_dir=result_root, show_image=True)
        
    except Exception as e:
        logger.info(e)

    

@app.route('/tracking_list',methods=['GET'])
def tracking_list():
    print("---tracking_list")
    #data = [random.randrange(1, 10, 1) for i in range(7)]
    data = get_online_ids()
    if data is not None:
        data.insert(0,'All')
    else:
        data = ['All']
    print(data)
    #return str(datetime.datetime.now())  # 示範用
    return jsonify(data)


@app.route('/get_select_id',methods=['GET','POST'])
def get_select_id():
    global get_data
    # send data to js
    if request.method == 'GET':
        print("---get_select_id: ",get_data)
        return str(get_data)

    # receive data from js and return 
    elif request.method == 'POST':
        print("---post_select_id: ", request.values['id'])
        get_data = request.values['id']
        if get_data is not 0:
            return jsonify(dict(id=get_data,)), 201



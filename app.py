
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

class opt:
    cfg = 'cfg/yolov3_1088x608.cfg'
    weights = 'weights/jde.1088x608.uncertainty.pt'
    iou_thres = 0.5
    conf_thres = 0.5
    nms_thres = 0.4
    min_box_area = 200
    track_buffer = 30
    output_root = 'static/data'

get_data = 0

@app.route('/',methods=['GET','POST'])
def index():
    # Get newest file path
    global get_data
    print("------index------")
    if request.method =='POST':
        if request.values['select_id']=='Selected':
            get_data = request.form.get('tracking_id')
            print("Select: ", get_data)
            return render_template('index.html',name=request.values['tracking_id'])
    
    return render_template('index.html',name="")


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
        eval_seq(opt, dataloader, 'mot', result_filename,
                save_dir=result_root, show_image=True)
        
    except Exception as e:
        logger.info(e)

    

@app.route('/api/test')
def test_page():
    data = [random.randrange(1, 10, 1) for i in range(7)]
    #data = get_online_ids()
    if data is not None:
        data.insert(0,'All')
    else:
        data = ['All']
    print(data)
    #return str(datetime.datetime.now())  # 示範用
    return jsonify(data)


@app.route('/get_select_id',methods=['GET','POST'])
def get_select_id():
    print("---get_select_id: ",get_data)
    #get_data = request.form.get('tracking_id')
    return str(get_data)


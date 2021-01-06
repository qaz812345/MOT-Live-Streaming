
import cv2
import logging
import argparse
import utils.datasets as datasets
from utils.utils import *
from utils.log import logger
from utils.timer import Timer
from utils.parse_config import parse_model_cfg
from track import eval_seq
from flask import Flask, render_template
app = Flask(__name__)

class opt:
    cfg = 'cfg/yolov3_1088x608.cfg'
    weights = 'weights/latest.pt'
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

def track(opt):
    # set saving dir
    result_root = opt.output_root if opt.output_root!='' else '.'
    mkdir_if_missing(result_root)

    # set configuration
    cfg_dict = parse_model_cfg(opt.cfg)
    opt.img_size = [int(cfg_dict[0]['width']), int(cfg_dict[0]['height'])]

    logger.info('Starting tracking...')
    # use camera to track
    dataloader = datasets.LoadCamera(img_size=opt.img_size)
    result_filename = os.path.join(result_root, 'results.txt')

    try:
        # start tracking
        eval_seq(opt, dataloader, 'mot', result_filename,
                 save_dir=result_root, show_image=True)
    except Exception as e:
        logger.info(e)
"""Demo file for running the JDE tracker on custom video sequences for pedestrian tracking.

This file is the entry point to running the tracker on custom video sequences. It loads images from the provided video sequence, uses the JDE tracker for inference and outputs the video with bounding boxes indicating pedestrians. The bounding boxes also have associated ids (shown in different colours) to keep track of the movement of each individual. 

Examples:
        $ python camera_tracking.py --weights path/to/model/weights --cfg path/to/model/cfg


Attributes:
    weights (str): Path from which to load the model weights. default='weights/latest.pt'
    cfg (str): Path to the cfg file describing the model. default='cfg/yolov3.cfg'
    iou-thres (float): IOU threshold for object to be classified as detected. default=0.5
    conf-thres (float): Confidence threshold for detection to be classified as object. default=0.5
    nms-thres (float): IOU threshold for performing non-max supression. default=0.4
    min-box-area (float): Filter out boxes smaller than this area from detections. default=200
    track-buffer (int): Size of the tracking buffer. default=30
    
"""
import cv2
import logging
import argparse
from utils.utils import *
from utils.log import logger
from utils.timer import Timer
from utils.parse_config import parse_model_cfg
import utils.datasets as datasets
from track import eval_seq


logger.setLevel(logging.INFO)

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

        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='demo.py')
    parser.add_argument('--cfg', type=str, default='cfg/yolov3_1088x608.cfg', help='cfg file path')
    parser.add_argument('--weights', type=str, default='weights/latest.pt', help='path to weights file')
    parser.add_argument('--iou-thres', type=float, default=0.5, help='iou threshold required to qualify as detected')
    parser.add_argument('--conf-thres', type=float, default=0.5, help='object confidence threshold')
    parser.add_argument('--nms-thres', type=float, default=0.4, help='iou threshold for non-maximum suppression')
    parser.add_argument('--min-box-area', type=float, default=200, help='filter out tiny boxes')
    parser.add_argument('--track-buffer', type=int, default=30, help='tracking buffer')
    parser.add_argument('--output-root', type=str, default='static/data', help='expected output root path')
    opt = parser.parse_args()
    print(opt, end='\n\n')

    track(opt)

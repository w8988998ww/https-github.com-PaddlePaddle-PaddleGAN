#  Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserve.
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

import argparse
import paddle

from ppgan.apps.dain_predictor import DAINPredictor
from ppgan.apps.deepremaster_predictor import DeepReasterPredictor
from ppgan.apps.deoldify_predictor import DeOldifyPredictor
from ppgan.apps.realsr_predictor import RealSRPredictor
from ppgan.apps.edvr_predictor import EDVRPredictor

parser = argparse.ArgumentParser(description='Fix video')
parser.add_argument('--input', type=str, default=None, help='Input video')
parser.add_argument('--output', type=str, default='output', help='output dir')
parser.add_argument('--DAIN_weight',
                    type=str,
                    default=None,
                    help='Path to model weight')
parser.add_argument('--DeepRemaster_weight',
                    type=str,
                    default=None,
                    help='Path to model weight')
parser.add_argument('--DeOldify_weight',
                    type=str,
                    default=None,
                    help='Path to model weight')
parser.add_argument('--RealSR_weight',
                    type=str,
                    default=None,
                    help='Path to model weight')
parser.add_argument('--EDVR_weight',
                    type=str,
                    default=None,
                    help='Path to model weight')
# DAIN args
parser.add_argument('--time_step',
                    type=float,
                    default=0.5,
                    help='choose the time steps')
# DeepRemaster args
parser.add_argument('--reference_dir',
                    type=str,
                    default=None,
                    help='Path to the reference image directory')
parser.add_argument('--colorization',
                    action='store_true',
                    default=False,
                    help='Remaster with colorization')
parser.add_argument('--mindim',
                    type=int,
                    default=360,
                    help='Length of minimum image edges')
# DeOldify args
parser.add_argument('--render_factor',
                    type=int,
                    default=32,
                    help='model inputsize=render_factor*16')
#process order support model name:[DAIN, DeepRemaster, DeOldify, RealSR, EDVR]
parser.add_argument('--proccess_order',
                    type=str,
                    default='none',
                    nargs='+',
                    help='Process order')

if __name__ == "__main__":
    args = parser.parse_args()

    orders = args.proccess_order
    temp_video_path = None

    for order in orders:
        print('Model {} proccess start..'.format(order))
        if temp_video_path is None:
            temp_video_path = args.input
        if order == 'DAIN':
            paddle.enable_static()
            predictor = DAINPredictor(args.output,
                                      weight_path=args.DAIN_weight,
                                      time_step=args.time_step)
            frames_path, temp_video_path = predictor.run(temp_video_path)
            paddle.disable_static()
        elif order == 'DeepRemaster':
            predictor = DeepReasterPredictor(
                args.output,
                weight_path=args.DeepRemaster_weight,
                colorization=args.colorization,
                reference_dir=args.reference_dir,
                mindim=args.mindim)
            frames_path, temp_video_path = predictor.run(temp_video_path)
        elif order == 'DeOldify':
            predictor = DeOldifyPredictor(args.output,
                                          weight_path=args.DeOldify_weight,
                                          render_factor=args.render_factor)
            frames_path, temp_video_path = predictor.run(temp_video_path)
        elif order == 'RealSR':
            predictor = RealSRPredictor(args.output,
                                        weight_path=args.RealSR_weight)
            frames_path, temp_video_path = predictor.run(temp_video_path)
        elif order == 'EDVR':
            paddle.enable_static()
            predictor = EDVRPredictor(args.output, weight_path=args.EDVR_weight)
            frames_path, temp_video_path = predictor.run(temp_video_path)
            paddle.disable_static()

        print('Model {} output frames path:'.format(order), frames_path)
        print('Model {} output video path:'.format(order), temp_video_path)
        print('Model {} proccess done!'.format(order))

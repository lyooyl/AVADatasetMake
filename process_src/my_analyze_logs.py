# Copyright (c) OpenMMLab. All rights reserved.
import argparse
import json
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# def plot_curve_val(log_dict, args):
#     if args.backend is not None:
#         plt.switch_backend(args.backend)
#     sns.set_style(args.style)
#     # if legend is None, use {filename}_{key} as legend
#     legend = args.legend
#     if legend is None:
#         legend = []
#         for metric in args.keys:
#             legend.append(f'{args.json_log}_{metric}')
#     assert len(legend) == len(args.keys)
#     metrics = args.keys

#     epochs = list(log_dict.keys())
#     plt.figure(figsize=(6, 4))
#     for j, metric in enumerate(metrics):
#         print(f'plot curve of {args.json_log}, metric is {metric}')
#         if metric not in log_dict[epochs[0]]:
#             raise KeyError(f'{args.json_log} does not contain metric {metric}')
#         xs = []
#         ys = []
#         if 'mAP/overall' in log_dict[epochs[0]]:
#             for epoch in epochs:
#                 xs.append(np.array([epoch]))
#                 ys.append(np.array([log_dict[epoch][metric]]))
#             label = 'epoch'
#         else:
#             raise KeyError(f'{args.json_log} does not contain metric {metric}')
#         xs = np.concatenate(xs)
#         ys = np.concatenate(ys)
#         plt.xlabel(label)
#         plt.plot(xs, ys, label=legend[j], linewidth=0.5, marker=".")
#         plt.legend()
#     if args.title is not None:
#         plt.title(args.title)
#     # plt.show()
#     if args.out is None:
#         plt.show()
#     else:
#         print(f'save curve to: {args.out}')
#         plt.savefig(args.out, dpi=300)
#         plt.cla()


def plot_curve_train(log_dict, log_dict_val, args):
    if args.backend is not None:
        plt.switch_backend(args.backend)
    sns.set_style(args.style)
    # if legend is None, use {filename}_{key} as legend
    legend = args.legend
    if legend is None:
        legend = []
        for metric in args.keys:
            legend.append(f'{args.json_log}_{metric}')
    assert len(legend) == len(args.keys)
    metrics = args.keys

    epochs = list(log_dict.keys())
    plt.figure(figsize=(6, 4))
    for j, metric in enumerate(metrics):
        print(f'plot curve of {args.json_log}, metric is {metric}')
        # if metric not in log_dict[epochs[0]]:
        #     raise KeyError(f'{args.json_log} does not contain metric {metric}')
        xs = []
        ys = []

        # val plot
        if metric in list(log_dict_val.values())[0]:
            epochs = list(log_dict_val.keys())
            for epoch in epochs:
                xs.append(np.array([epoch]))
                ys.append(np.array([log_dict_val[epoch][metric]]))
            label = 'epoch'

        # train plot
        if metric in log_dict[epochs[0]]:
            for epoch in epochs:
                iters = log_dict[epoch]['step']
                xs.append(np.array(iters))
                ys.append(np.array(log_dict[epoch][metric][:len(iters)]))
            label = 'iter'
        xs = np.concatenate(xs)
        ys = np.concatenate(ys)
        plt.xlabel(label)
        plt.plot(xs, ys, label=legend[j], linewidth=0.5, marker=".")
        plt.legend()
    if args.title is not None:
        plt.title(args.title)
    # plt.show()
    if args.out is None:
        plt.show()
    else:
        print(f'save curve to: {args.out}')
        plt.savefig(args.out, dpi=300)
        plt.cla()


def load_json_logs(json_log):
    log_dict = dict()
    log_dict_val = dict()
    with open(json_log, 'r') as log_file:
        for line in log_file:
            log = json.loads(line.strip())
            # skip lines without `epoch` field
            if 'epoch' in log:
                epoch = log.pop('epoch')
                if epoch not in log_dict:
                    log_dict[epoch] = defaultdict(list)
                for k, v in log.items():
                    log_dict[epoch][k].append(v)
            if 'mAP/overall' in log:
                epoch_val = log.pop('step')
                if epoch_val not in log_dict_val:
                    log_dict_val[epoch_val] = defaultdict(list)
                for k, v in log.items():
                    log_dict_val[epoch_val][k].append(v)

    return log_dict, log_dict_val


def plot_parser() -> object:
    parser_plt = argparse.ArgumentParser(description='Analyze Json Log: parser for plotting curves')
    parser_plt.add_argument(
        '--json_log',
        default="../work_dirs/slowfast_det_rec_drinkWater/20230725_165852/vis_data/scalars.json",
        type=str,
        help='path of train log in json format')
    parser_plt.add_argument(
        '--keys',
        type=str,
        nargs='+',
        default=['mAP/overall'],  # , ['mAP/overall'] ['loss', 'prec@top1','recall@top1', "grad_norm"],
        help='the metric that you want to plot')
    parser_plt.add_argument('--title', type=str, help='title of figure')
    parser_plt.add_argument(
        '--legend',
        type=str,
        nargs='+',
        default=['mAP'],
        help='legend of each plot')
    parser_plt.add_argument(
        '--backend', type=str, default=None, help='backend of plt')
    parser_plt.add_argument(
        '--style', type=str, default='dark', help='style of plt')
    parser_plt.add_argument(
        '--out', type=str, default='mAP.jpg')
    return parser_plt.parse_args()


def main():
    args = plot_parser()

    json_log = args.json_log
    assert json_log.endswith('.json')

    log_dict, log_dict_val = load_json_logs(json_log)

    plot_curve_train(log_dict, log_dict_val, args)
    # plot_curve_val(log_dict_val, args)


if __name__ == '__main__':
    main()

"""Build the Glot500 training corpus from per-language HuggingFace datasets.

Self-contained (replaces merge_files.sh): the argument defaults below reproduce
the old shell invocation, so you can run it directly:

    python merge_files.py                 # uses the baked-in defaults
    python merge_files.py --scale 5       # override any default on the CLI

Reads ../miscellaneous/languages_stats_lowres.csv (resolved relative to this
file), skipping '#'-commented language rows.
"""
import argparse
import codecs
import copy
import json
import logging
import os
import random
import sys
from datetime import datetime
from os import listdir

import pandas as pd
from datasets import load_from_disk



# def write_file(input_fname, output_f, num):
#     dataset = load_from_disk(input_fname)
#     indexs = random.choices(list(range(len(dataset['train']))), k=num)
#     for index in indexs:
#         output_f.write('%s\n' % (dataset['train'][index]['text']))

def write_file(input_fname, output_f, num):
    print(f'  loading {input_fname} ({num} samples)...', flush=True)   # ← NEW (line 18)
    dataset = load_from_disk(input_fname)
    indexs = random.choices(list(range(len(dataset['train']))), k=num)
    for index in indexs:
        output_f.write('%s\n' % (dataset['train'][index]['text']))
    print(f'  done {input_fname}', flush=True)                          # ← NEW (line 23)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_directory', type=str, default='/disk3/moon/Glot500/data/raw/')
    parser.add_argument('--save_directory', type=str, default='/disk3/moon/Glot500/data/')
    parser.add_argument('--experiment_name', type=str, default='Glot500_bible')
    parser.add_argument("--lg_sampling_factor", type=float, default=0.3, help="Language sampling factor")
    parser.add_argument("--scale", type=float, default=30, help="controls the minimum number of sentences of each language")

    args = parser.parse_args()

    unseen_lg2count = {}
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'miscellaneous', 'languages_stats_lowres.csv')
    df = pd.read_csv(csv_path, comment='#')
    df.columns = df.columns.str.strip()  # header has a stray leading space in ' new_length'
    unseen_lg2count = {str(lg) + '_' + script.replace("['", "").replace("']", ""): count 
       for lg, script, count, is_seen in zip(df['language'], df['script'], df['new_length'], df['XLM-R']) if is_seen is not True}
    seen_lg2count = {str(lg) + '_' + script.replace("['", "").replace("']", ""): count 
       for lg, script, count, is_seen in zip(df['language'], df['script'], df['new_length'], df['XLM-R']) if is_seen is True}
    print('%s unseen languages and %s seen languages' % (len(unseen_lg2count), len(seen_lg2count)))

    # downsample (S < 1) or upsample (S>1) the importance of high-resource languages
    S = args.lg_sampling_factor
    unseen_tot = sum([unseen_lg2count[lg] for lg in unseen_lg2count])
    unseen_tot_S = sum([unseen_lg2count[lg]**S for lg in unseen_lg2count])

    # minimum count and minimum probability
    min_c = min([unseen_lg2count[lg] for lg in unseen_lg2count])
    min_p = min([unseen_lg2count[lg]**S for lg in unseen_lg2count]) / unseen_tot_S
    tot_before_seen = sum([seen_lg2count[lg] for lg in seen_lg2count])
    tot_before_unseen = unseen_tot
    tot_after_seen = int(args.scale * min_c) * len(seen_lg2count)
    tot_after_unseen = sum([int(args.scale * min_c * (unseen_lg2count[lg]**S / unseen_tot_S / min_p)) for lg in unseen_lg2count])
    tot_before = tot_before_seen + tot_before_unseen
    tot_after = tot_after_seen + tot_after_unseen
    print('before resampling: %d sentences (%d for seen, %d for unseen) - after resampling: %d (%d for seen, %d for unseen)' % (tot_before, tot_before_seen, tot_before_unseen, tot_after, tot_after_seen, tot_after_unseen))
    print()

    for lg, count in unseen_lg2count.items():
        p = unseen_lg2count[lg]**S / unseen_tot_S
        print('%s -unseen_lg2count: before resampling: %.2f, %d - after resampling: %.2f, %d' % (lg, 100.0 * unseen_lg2count[lg] / tot_before, unseen_lg2count[lg], 100.0 * p, int(args.scale * min_c * (p / min_p))))
    for lg, count in seen_lg2count.items():
        print('%s -seen_lg2count: before resampling: %d - after resampling[chopped to 30*min_c]: %d' % (lg, seen_lg2count[lg], int(args.scale * min_c)))

    # scale:
    output_fname = args.save_directory + args.experiment_name + '.txt'
    output_f = codecs.open(output_fname, 'w', encoding='utf-8')
    # Load files of seen langs for training tokenizer
    
    for lg in seen_lg2count:
        input_fname = args.data_directory + lg
        if not os.path.isdir(input_fname):
            print(f'seen:SKIP (missing on disk): {lg}')
            continue
        write_file(input_fname, output_f, int(args.scale * min_c))
    # Load files of unseen langs for training tokenizer
    
    for lg in unseen_lg2count:
        input_fname = args.data_directory + lg
        if not os.path.isdir(input_fname):
            print(f'SKIP (missing on disk): {lg}')
            continue
        p = unseen_lg2count[lg]**S / unseen_tot_S
        write_file(input_fname, output_f, int(args.scale * min_c * (p / min_p)))
    print(f'preprocessing corpuses is finished')
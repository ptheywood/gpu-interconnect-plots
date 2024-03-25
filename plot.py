#! /usr/bin/env python3
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pathlib


MONOSPACE_FONT_FAMILY = "DejaVu Sans Mono"

class Config:
    def __init__(self):
        self.SNS_CONTEXT = "talk"
        self.SNS_STYLE = "darkgrid"
        self.SNS_PALETTE = "Dark2"
        self.FIGSIZE_INCHES = (16, 9)
        self.DPI = 96
        self.X = "label"
        self.XLABEL = "Interconnefct"
        self.Y = "peak bidirectional bandwidth (GB/s)"
        self.YLABEL = "Peak Bandwidth (GB/s)"
        self.YLIM_BOTTOM = None
        self.HUE = "manufacturer"
        self.HUELABEL="Manufacturer"
        self.STYLE = "manufacturer"
        self.STYLELABEL="Manufacturer"
        self.LEGEND_BORDER_PAD = 0.5
        self.EXTERNAL_LEGEND = False

def plot(args):
    config = Config()

    df = pd.read_csv(args.input)
    print(args)

    # Do some plotting stuff.
    sns.set_context(config.SNS_CONTEXT, rc={"lines.linewidth": 2.5})  
    sns.set_style(config.SNS_STYLE)
    huecount = len(df[config.HUE].unique()) if config.HUE is not None else 1 
    palette = sns.color_palette(config.SNS_PALETTE, huecount)
    sns.set_palette(palette)

    fig, ax = plt.subplots(constrained_layout=True)
    fig.set_size_inches(config.FIGSIZE_INCHES[0], config.FIGSIZE_INCHES[1])


    g = sns.barplot(
        data=df, 
        x=config.X,
        y=config.Y, 
        hue=config.HUE, 
        ax=ax,
        palette=palette,
    )

    # Axis settings
    if config.XLABEL:
        ax.set(xlabel=config.XLABEL)
    if config.YLABEL:
        ax.set(ylabel=config.YLABEL)

    title="@todo"
    ax.set_title(title)

    if args.output:
        if args.output.is_dir():
            raise Exception(f"{args.output} is a directory")
        elif args.output.is_file() and not args.force:
            raise Exception(f"{args.is_file} is an existing file. Use -f/--force to overwrite")
        # Save the figure to disk, creating the parent dir if needed.
        args.output.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(args.output, dpi=config.DPI, bbox_inches='tight')
    else:
        plt.show()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=pathlib.Path, help="input csv path")
    parser.add_argument("-o", "--output", type=pathlib.Path, help="output image path. shows if omitted")
    parser.add_argument("-f", "--force", action="store_true", help="Overwrite existing output files")
    parser.add_argument("--title", type=str, help="Figure title")
    args = parser.parse_args()
    plot(args)

if __name__ == "__main__":
    main()
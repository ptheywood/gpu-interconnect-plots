#! /usr/bin/env python3
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
import seaborn as sns
import pathlib


MONOSPACE_FONT_FAMILY = "DejaVu Sans Mono"

class Config:
    def __init__(self):
        self.SNS_CONTEXT = "talk"
        self.SNS_STYLE = "darkgrid"
        self.SNS_PALETTE = "Dark2"
        self.FIGSIZE_INCHES = (12, 7)
        self.DPI = 96
        self.X = "label"
        self.XLABEL = "Interconnect"
        self.Y = "peak bidirectional bandwidth (GB/s)"
        self.YLABEL = "Peak Bandwidth (GB/s)"
        self.YLIM_BOTTOM = None
        self.HUE = "technology"
        self.HUELABEL="Technology"
        self.BAR_LABEL="model"
        self.STYLE = self.HUE
        self.STYLELABEL= self.HUELABEL
        self.LEGEND_BORDER_PAD = 0.5
        self.EXTERNAL_LEGEND = False
        self.Y_TICK_MULTIPLE_LOCATOR=100

def plot(args):
    config = Config()

    df = pd.read_csv(args.input,keep_default_na=False)

    # Do some plotting stuff.
    sns.set_context(config.SNS_CONTEXT, rc={"lines.linewidth": 2.5})  
    sns.set_style(config.SNS_STYLE)
    huecount = len(df[config.HUE].unique()) if config.HUE is not None else len(df) 
    palette = sns.color_palette(config.SNS_PALETTE, huecount)
    if config.HUE == "technology" and len(palette) == 3:
        palette = [palette[2], palette[0], palette[1]]
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
        dodge=False,
    )

    if args.bar_label:
        if args.bar_label is None or args.bar_label in df:
            config.BAR_LABEL=args.bar_label

    # add bar labels
    for container, hue_v in zip(ax.containers, df[config.HUE].unique()):
        labels = df.query(f'{config.HUE}=="{hue_v}"')[config.BAR_LABEL] if config.BAR_LABEL is not None else None
        ax.bar_label(container, labels=labels)#, label_type='center')

    # Axis settings
    if config.XLABEL:
        ax.set(xlabel=config.XLABEL)
    if config.YLABEL:
        ax.set(ylabel=config.YLABEL)

    if config.Y_TICK_MULTIPLE_LOCATOR:
        ax.yaxis.set_major_locator(ticker.MultipleLocator(config.Y_TICK_MULTIPLE_LOCATOR))


    title="GPU Host-Device Interconnect Bandwidth"
    ax.set_title(title)

    # compute the legend label
    legend_title = f"{config.HUELABEL} x {config.STYLELABEL}" if config.HUELABEL != config.STYLELABEL else f"{config.HUELABEL}"
    # If using an external legend, do external placement. This is experimental.
    if config.EXTERNAL_LEGEND:
        # Set legend placement if not internal.
        loc = "upper left"
        # @todo - y offset should be LEGEND_BORDER_PAD transformed from font units to bbox.
        bbox_to_anchor = (1, 1 - 0.0)
        handles, labels = ax.get_legend_handles_labels()
        # add an invisble patch with the appropriate label, like how seaborn does if multiple values are provided.
        handles.insert(0, mpatches.Rectangle((0,0), 1, 1, fill=False, edgecolor='none', visible=False, label=hs_label))
        labels.insert(0, legend_title)
        legend = ax.legend(handles=handles, labels=labels, loc=loc, bbox_to_anchor=bbox_to_anchor, borderaxespad=config.LEGEND_BORDER_PAD)
        plt.setp(legend.texts)
    else:
        if ax.get_legend() is not None:
            legend = ax.get_legend()
            legend.set_title(legend_title)
            plt.setp(legend.texts);

    if args.output:
        if args.output.is_dir():
            raise Exception(f"{args.output} is a directory")
        elif args.output.is_file() and not args.force:
            raise Exception(f"{args.output} is an existing file. Use -f/--force to overwrite")
        # Save the figure to disk, creating the parent dir if needed.
        args.output.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(args.output, dpi=config.DPI, bbox_inches='tight')
    else:
        plt.show()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=pathlib.Path, help="input csv path", required=True)
    parser.add_argument("-o", "--output", type=pathlib.Path, help="output image path. shows if omitted")
    parser.add_argument("-f", "--force", action="store_true", help="Overwrite existing output files")
    parser.add_argument("--title", type=str, help="Figure title")
    parser.add_argument("--bar-label", type=str, help="CSV column to use for the bar label")
    args = parser.parse_args()
    plot(args)

if __name__ == "__main__":
    main()
# CScreener

CScreener is a PySide6-based GUI for processing the CNMFE preprocessing output in calcium imaging videos. There are many other all inclusive CNMFE toolkits, but this app is designed to be a light-weight solution for visualizing and screening the MATLAB outputs from the popular CNMFE-based calcium imaging processing toolkit [MiniscopeAnalysis](https://github.com/etterguillaume/MiniscopeAnalysis). The general purpose is to allow users to go through ROIs, compare and determine which ones are good cells and which ones are false or duplicated signals.

By default, the output of CNMFE is a MATLAB structure `ms` that contains these key fields:

- FiltTraces
- RawTraces
- S (Inferred Spikes from deconvolution)
- SFPs (ROI footprints)
- numNeurons

These fields are required for CScreener to correctly load the `ms.mat`. Additionally, if the `ms.mat` is saved in `-v7.3` format in MATLAB, it is best to create a field named 'cell_label' containing a numNeurons x 1 all-ones vector. If `ms.mat` is saved in `-v7.0` or earlier format, CScreener will create 'cell_label'.

The PySide CScreener has several advantages comparing to its [MATLAB predecessor](https://github.com/hsingchien/1p_preprocessing):

- Faster video loading using OpenCV.
- Smoother experience with heavy computing tasks such as computing the maximum projection frame handled by a separate thread, making the app responsive to user actions even during computation.
- More functions with efficient use of space, more figures, and information organized in tables and tabs.
- Scalable with the possibility to add more functions and modules in the future.

## Installation

Clone the repository. Navigate to root folder in Anaconda Prompt. Create the conda environment from environment.yml.

```bash
conda env create --file environment.yml
```

Activate the cscreener environment. Navigate to setup.py, install the package

```bash
conda activate cscreener
python setup.py install
```

## Usage

Open the app from anaconda prompt

```python
screen-cell
```

![Alt text](cscreener/image/screenshot_lowdf.png)

Load video and mat file.
To focus on a particular cell, you can use either of the following methods:  
(1). Double click the row in the Cell Table 1
(2). Double click the contour in the Image Frame 2  
Once a cell activated, it will be highlighted in orange in the Cell Table 1.

To zoom in on the focused cell, use the zoom slider
To adjust the contour size, use the contour slider
You can sort the cells by clicking the column header in the Cell Table 2, or more conveniently, by using keyboard shortcuts:

- ID: `A`
- Correlation: `S`
- Distance: `D`
- dFF: `F`

To select a companion cell for comparison with the focused cell, double-click its entry in Cell Table 2.  
Use `I/K` to move up and down in Cell Table 1; `O/L` to move up and down in Cell Table 2. If none are activated, `K/L` activates first row, `I/O` activates the last row. You can jump to the maximum intensity frame of the focused cell by pressing `B`, and to the maximum intensity frame of the companion cell by pressing `N`. To toggle the label of the focused cell, press `G`, and to toggle the label of the companion cell, press `H`.

Cell Table 2 supports multi-selection. Selected cells are previewed in image frame 1, and their contours can be added to the display by clicking the `Add to display` button. The added cells will be highlighted in blue.

Cell Table 2 also colors the entries by the number of user visits. Entries that have been visited 1-2 times are colored light green/red, those visited 3-4 times are colored medium green/red, and those visited more than 5 times are colored dark green/red. To reset the number of visits, click the header of the `Label` column.

It is recommended to use `ms.mat` in `v7.0` format. SciPy does not provide support for `v7.3` mat files. For large `v7.3` mat files (>2GB), writing on the original file ("Save to MS") through h5py is the only option, in which case the original file needs to have a field named 'cell_label' containing a numNeurons x 1 all-ones vector, otherwise the saving may fail or the saved cell labels may not be readable by MATLAB. Writing is limited to the cell_label field, and the writing access is only opened in saving, which is instantaneous, so the risk of corrupting the original file is minimal.

Below are detailed explanations for different saving options and which one you should use.

To deal with the complexity of different versions of .mat file, CScreener provides multiple options for exporting ms files:  
`Export MS` is available when current MS file is `v7.0` or earlier. It will save a copy.
`Save to MS` is for `v7.3` mat files. modifying the cell label of the original MS file. The MS file must have a native field named 'cell_label' containing a number_of_cells x 1 all-ones vector, or the save will fail.  
`Save Lean MS` tries to save the MS file with only the necessary info: FiltTraces, RawTraces, Spikes, Contours (SFPs), cell_label in `v7.0`. Saving fails if the file is too large (>2 GB)  
`Export Label as CSV` is the last resort if `Saving to MS` fails. This option works for all scenarios.

## Contributing

I am currently writing test cases, which will be added to the repository soon

If you would like to contribute, please feel free to fork this repository and test your edits. Once you have tested your changes, you can create a pull request and I will review it as soon as possible.

<!--
## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.-->

## License

[MIT](https://choosealicense.com/licenses/mit/)

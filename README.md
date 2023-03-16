# CScreener

CScreener is a remake of my old MATLAB cell picking GUI designed to process the CNMFE(Constrained Nonnegative Matrix Factorization) preprocessing output for calcium imaging videos. There are several advantages this remake holds over the old MATLAB app (which is also why I remade it):

- Much faster video loading thanks to opencv.
- Much smoother experience. Heavy computing tasks like computing the maximum projection frame is handled by a separate thread so the app is responsive to user action even during computing.
- More functions. The space was used more efficiently with more figures and information organized in tables and tabs.
- More possibilities. The app is built with PySide6, making it very scalable. More functions and modules can be easily added in the future.

There is one drawback. Because of the lack of support for `v7.3` mat files in python, the app only supports direct writing on large (>2GB) mat files through h5py. Although writing ("Save to MS") in such situation is limited to the cell_label field, it is strongly recommended to make backup mat before start.

## Installation

Clone the repository. Navigate to root folder in Anaconda Prompt. Create the conda environment from environment.yml.

```bash
conda env create --file environment.yml
```

Navigate to find setup.py, install the package

```bash
python setup.py install
```

## Usage

Open the app from anaconda prompt

```python
screen-cell
```

![Alt text](cscreener/image/screenshot.png)

In file menu, load video and mat file.
Focus on cell by one of the following methods:  
(1). double clicking the row in the cell table 1 (the one on the left)
(2). double clicking the contour in the overview image  
Once activated, the cell will be highlighted in orange in cell table 1. `I/K to move up/down cell table 1`

Zoom into the focused cell using zoom slider
Adjust the contour size using contour slider
Sort the cells by clicking the column header in cell table 2. Keyboard shortcut for sorting by each column are:  
`ID = A; Correlation = S; Distance = D; dFF = F`  
Select the companion cell you want to compare with the focus cell by double clicking its entry in the cell table 2. `Press O/L to move up/down the cell table 2`. When none are activated, I/O activates first in the table and K/L activates last in the table.  
`Jump to maximum intensity frame of focus cell = B, of companion cell = N`  
`G = Toggle label of focus cell`, `H = Toggle label of companion cell`

Cell table 2 support multi selection. Selected cells are previewed in image 1. The contours can be added to display by clicking the `Add to display` button. The added cells will be highlighted in blue.

Modified mat file can be saved through File menu.

Cell table 2 also colors the entries by the number of user visists. 1-2 visits = light, 3-4 = medium, >5 = dark. To reset the number of visits, click the header of `Label` column.

<!--
## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.-->

## License

[MIT](https://choosealicense.com/licenses/mit/)

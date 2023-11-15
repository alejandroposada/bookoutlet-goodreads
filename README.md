# bookoutlet_goodreads
Find what books from your Goodreads to-read list are available in Bookoutlet.


## How to use
Set-up (Python >= 3.6)
```
pip install -r requirements.txt
```

Usage:
```
usage: run.py [-h] --csv CSV --output OUTPUT --threshold THRESHOLD

Search for books on bookoutlet

optional arguments:
  -h, --help            show this help message and exit
  --csv CSV             Path to the CSV file
  --output OUTPUT       Path to the output file
  --threshold THRESHOLD Fuzzy threshold for searching
```

The program will find the matches and write them to a file.

Example:
```
python run.py --csv my_lib.csv --output output.txt --threshold 98
```

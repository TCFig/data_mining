# Metacyc Pathway Taxonomic Range Scraper
This repository contains a Python script that logs into the Metacyc website, fetches the expected taxonomic range for a list of pathway IDs, and saves the data to a file. The script uses the Helium library for browser automation to log in, navigate, and retrieve information from the Metacyc web interface.

## Files
- `fetch_taxonomic_range.py`: The main script for logging into Metacyc, retrieving taxonomic range data, and saving results.
- `test_input.txt`: An example file to test the script. This file should contain one Metacyc pathway ID per line.

Prerequisites
- Python 3.x
- [Helium](https://github.com/mherrmann/helium) for browser automation.
- Google Chrome browser (Helium currently only supports Chrome).
- ChromeDriver executable compatible with your Chrome version (Helium will typically handle this automatically).

## Usage
**1. Prepare input file:** Create a text file (e.g., `Metacyc_pathID.txt`) containing Metacyc pathway IDs, one per line.

**2. Run the script:**

```bash
python get_pathID_taxon.py <username> <password> <input_file> <output_file>
```
- `<username>`: Your Metacyc username.
- `<password>`: Your Metacyc password.
- `<input_file>`: Path to the file containing pathway IDs (one per line).
- `<output_file>`: Path to the output file where results will be saved.

**3. Output:** The script will create or append to the specified output file in a tab-separated format with the following columns:

- `Pathway_ID`: The pathway ID from Metacyc.
- `Expected_Taxonomic_Range`: The taxonomic range associated with each pathway.


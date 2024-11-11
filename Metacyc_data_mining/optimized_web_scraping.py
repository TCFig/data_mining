from helium import *
import time
import argparse
import os

def log_in(user, password):
    """Logs into the Metacyc website."""
    start_chrome("https://biocyc.org/pathway?orgid=META&id=PWY-1042")
    click("Login")
    write(user, into='Username')
    write(password, into='Password')
    click('LOGIN')
    time.sleep(5)

def get_taxonomic_range(pathway_id):
    """Fetches the taxonomic range for a given pathway ID."""
    go_to(f"https://biocyc.org/pathway?orgid=META&id={pathway_id}")
    press(PAGE_DOWN)
    time.sleep(2)
    organism_list = find_all(S('//*[@id="SUMMARY"]/div[3]/div[1]/p[2]'))
    taxonomic_range = [item.web_element.text for item in organism_list]
    if not taxonomic_range:
        print('Metacyc has reached the limit of searches.')
        return ""
    return str(taxonomic_range).replace('Expected Taxonomic Range:', '').strip()

def get_last_processed_id(outfile_path):
    """Gets the last processed pathway ID from the output file."""
    if not os.path.exists(outfile_path) or os.stat(outfile_path).st_size == 0:
        return None
    with open(outfile_path, 'r') as outfile:
        lines = outfile.readlines()
        if lines:
            return lines[-1].split('\t')[0]
    return None

def main(args):
    infile = args.input_file
    outfile_path = args.output_file.name

    try:
        log_in(args.user, args.password)
        last_processed_id = get_last_processed_id(outfile_path)
        start_processing = not last_processed_id

        with open(infile.name, 'r') as infile, open(outfile_path, 'a') as outfile:
            if os.stat(outfile_path).st_size == 0:
                outfile.write("Pathway_ID\tExpected_Taxonomic_Range\n")

            for line in infile:
                pathway_id = line.strip()
                if not start_processing:
                    if pathway_id == last_processed_id:
                        start_processing = True
                    continue

                taxonomic_range = get_taxonomic_range(pathway_id)
                if not taxonomic_range:
                    print("No more taxonomic range data, stopping.")
                    break

                outfile.write(f"{pathway_id}\t{taxonomic_range}\n")
                print(f"Processed {pathway_id}: {taxonomic_range}")

    finally:
        kill_browser()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get the Expected Taxonomic Range for a pathway ID in Metacyc.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('user', type=str, help='Username for Metacyc login')
    parser.add_argument('password', type=str, help='Password for Metacyc login')
    parser.add_argument('input_file', type=argparse.FileType('r'), help='Input file with Metacyc IDs')
    parser.add_argument('output_file', type=argparse.FileType('a+'), help='Output TSV file')

    args = parser.parse_args()
    main(args)

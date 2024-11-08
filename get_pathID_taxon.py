from helium import *
import time
import argparse
import os

def log_in(user, password):
    """Logs into the Metacyc website."""
    start_chrome(f"https://biocyc.org/pathway?orgid=META&id=PWY-1042")
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
        return ""  # Return empty string instead of True
    else:
        return str(taxonomic_range).replace('Expected Taxonomic Range:', '').strip()

def main(args):

    infile = args.input_file
    outfile_path = args.output_file.name

    try:
        # Log in to the website
        log_in(args.user, args.password)
        
        # Fetch data and write to output
        with open(outfile_path, 'a') as outfile:
            if os.stat(outfile_path).st_size == 0:                       # If file is empty or non-existent
                outfile.write("Pathway_ID\tExpected_Taxonomic_Range\n")  # Write header if new file

            for line in infile:
                pathway_id = line.strip()
                taxonomic_range = get_taxonomic_range(pathway_id)

                if taxonomic_range == "":
                    print("No more taxonomic range data, stopping.")
                    break

                outfile.write(f"{pathway_id}\t{taxonomic_range}\n")
                print(f"Processed {pathway_id}: {taxonomic_range}")

    finally:
        # Ensure Chrome is closed at the end of the script
        kill_browser()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get the Expected Taxonomic Range associated \
                                     to a pathway ID in Metacyc.", \
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('user', type=str, help='Username used to login to Metacyc')
    parser.add_argument('password', type=str, help='Password used to login to Metacyc')
    parser.add_argument('input_file', type=argparse.FileType('r'), \
                        help='Input file containing the Metacyc IDs')
    parser.add_argument('output_file', type=argparse.FileType('a+'), \
                        help = 'Output tsv file')

    args = parser.parse_args()
    main(args)

import os
import re

# TODO: ricordati che 1 file su 3 ha un </rdf:RDF> finale in più
def clean_rdf_file(file_path: str, final_path: str, last_words):
    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Read the file contents into a list
        lines = file.readlines()

    # Open the file in write mode
    with open(final_path, 'w') as file:
        # Iterate over the lines in the list
        for line in lines:
            # Use regular expression to check if the line contains the sequence of characters "ds::-"
            match = re.search(r'ds::-', line)
            # If the line does not contain the sequence of characters, write it to the file
            if match is None:
                file.write(line)
            else:
                if re.search(last_words, line) is not None:
                    file.write("</rdf:Description>\n")
        file.write("</rdf:RDF>")


paths = {"dataset/shoot.rdf": "<ds::-computed_region_d9mm_jgwp>",
         "dataset/arrests.rdf": "<ds::-computed_region_43wa_7qmu>",
         "dataset/crimes.rdf": "<ds::-computed_region_d3ds_rm58>"}

for path, last_words in paths.items():
    final_path = "clean_" + path
    clean_rdf_file("../" + path, "../" + final_path, last_words)

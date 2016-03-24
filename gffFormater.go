/*
* Work on parallel processing
*
*
 */
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"strconv"
)

func main() {

	// Printing to the command line
	// fmt.Println(buildCorrectedGFF("incorrectFormat.gff"))

	// Call buildCorrectedGFF
	buildCorrectedGFF("inccorectlyFormated.gff")
}

/*
* This function will attempt to correct a given GFF files format, according to the GFF3 specifications maintained by The Sequence Oncology Project
* @params: a string representing the path for the gff file to be formatted
*/
func buildCorrectedGFF(path string) {
	// Run function readlines to read in data
	data, err := readLines(path)

	// Print error if it arises
	if err != nil {
		fmt.Println(err)
	}

	// A slice to hold our corrected data
	var correctedLines []string
	// Counter to give lines unique ID's if neccecary
	IDCounter := 0

	// A for each loop to move through each line of the GFF
	for _, lines := range data {

		// Split each line at its tab
		splitAtTab := strings.Split(lines, "\t")

		// Stores the element of each line
		element := splitAtTab[2]

		// Iterate through ever line. Save each one in memory that is not a "start_codon" or "stop_codon" item.
		if element == "gene" || element == "CDS" || element == "exon" || element == "mRNA"|| element == "UTR" || element == "rRNA" {

			// Split up the attributes at each semicolon
			attributes := strings.Split(splitAtTab[8], "; ")

			// Add back in the semicolon for each attribute
			for index, attribute := range attributes {
				attributes[index] = attribute + ";"
			}

			
			/*THIS WAS WRITTEN LIKE THIS TO SAVE TIME. ASSUMES THAT THE GFF HAS AN INCORRECTLY FORMATED NAME ATTRIBUTE*/
			/*TO HANDLE MORE CASES, IF STATEMENTS LIKE THE ONE BELOW THAT CHECKS FOR AN ID SHOULD BE WRITTEN*/

			// Fixes the name attribute
			name_attribute := strings.Split(attributes[0], " ")
			attributes[0] = "Name=" + name_attribute[1]


			// Checks if attributes have an ID. If not prepends it to attributes
			if !(stringInSlice("ID", attributes)) {
				// Need a counter for each of the element types
				IDCounter += 1
				// Prepend unique ID to attributes
				attributes = append([]string{"ID=" + element + strconv.Itoa(IDCounter) +";"}, attributes...)
			}


			// Loops through attributes and replaces all spaces with = signs
			for index, _ := range attributes {
				attributes[index] = strings.Replace(attributes[index], " ", "=", 1)
			}
			
			/*THIS IS WHERE THE CORRECTED LINES ARE APPENED TO A SLICE*/

			// This will append each line of data, from coloums 0 to 7, and then the fixed attributes, followed by a newline, to corrected lines
			correctedLines = append(correctedLines, strings.Join(append(splitAtTab[:8]), "\t"))
			correctedLines = append(correctedLines,"\t")
			correctedLines = append(correctedLines, attributes...)
			correctedLines = append(correctedLines,"\n")


		} else {fmt.Println("Line element does not follow GFF3 convention: \n" + lines)}
		
	}

	// If the GFF file has no GFF version, this will append a directive to the beginning of the file.
	if !(strings.Contains(correctedLines[0], "##gff-version")) {
	correctedLines = append([]string{"##gff-version\t3\n"}, correctedLines...)
	}

	// Write the corrected lines to a file
	writeFile(path, correctedLines)
}


/*
* This function will return true if any elements in a input slice of strings, list, contains a substring, a, and false otherwise
* @params: a: substring to search for in the slice of strings
* @params list: a slice of strings to query
* @return true if any element of list[] contains string a.
*/

func stringInSlice(a string, list []string) bool {
    for _, b := range list {
        if strings.Contains(b,a) {
            return true
        }
    }
    return false
}

/*
 * This function will write the corrected GFF file, as returned by buildCorrectedGFF as a string splice, to a created file named 
 * <name of input file>_CORRECTED.gff" in the same directory the program was ran
 * @params: a string representing the path for the GFF file to be formatted
 * @return any error returned by the WriteString function.
 */
func writeFile(path string, sliceToWrite []string) (int, error) {
	
	// From the file path, produces a string with its name.gff changed to name_CORRECTED.gff
	// Savs this as newFilenameString
	newFilenameSlice := strings.Split(path, "/")
	newFilenameSlice = strings.Split(newFilenameSlice[len(newFilenameSlice)-1], ".")
	newFilenameSlice[0] = newFilenameSlice[0] + "_FORMATFIXED"
	newFilenameString := strings.Join(append(newFilenameSlice), ".")

	f, err := os.Create(newFilenameString)
	// Defer closing of the file
	defer f.Close()
	// Create new Writer object
	writer := bufio.NewWriter(f)
	// Write each line of the returned []string array containing the corrected lines of the GFF file at path
	n4, err := writer.WriteString(strings.Join(append(sliceToWrite), ""))
	return n4, err
}

/*
* Function will open GFF file and store it in memory
* @params: a string representing the path for the GFF file to be formatted
* @return: a string splice containing each line of the GFF file, and any errors reported by the compiler
 */
func readLines(path string) ([]string, error) {

	// Open the file
	file, err := os.Open(path)

	// Catch any erros
	if err != nil {
		return nil, err
	}

	// Close the file only if it was opened successfully and there are no errors
	defer file.Close()

	// Declare a splice to store each line of the GFF file
	var lines []string

	// Create new scanner object for the file
	scanner := bufio.NewScanner(file)

	// Scan the file using our scanner object. Append each line to splice lines
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	return lines, scanner.Err()
}

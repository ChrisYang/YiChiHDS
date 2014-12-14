#include <fstream>
#include <algorithm>
#include <iterator>
#include <iostream>
#include <string>
#include <cstdlib>
#include <vector>
#include <map>
int main(int argc, char **argv) {
    if (argc < 2) {
        std::cerr << "Usage: program <infile>\n";
        return -1;
    }

    std::ifstream infile(argv[1]); // This is used to open a file 
    if (!infile.is_open()) return -1; //check whether it is opened or not 

    std::map<char, int> wordCount;// define a map from string to int 
    char c;
    while (infile >> c)//read a character from the file 
    {
    	std::cout << c << std::endl;// display the character 
    	++wordCount[c];//add count of the word 
    }
    for (std::map<char, int>::iterator it = wordCount.begin(); it != wordCount.end(); ++it)
     {
           std::cout << it->first <<" : "<< it->second << std::endl;//display the frequency, we can write the output to a file 
     }
    return 0;
}
#include <fstream>
#include <algorithm>
#include <iterator>
#include <iostream>
#include <string>
#include <cstdlib>
#include <vector>
#include <map>
#include <locale>


int main(int argc, char **argv) {
    if (argc < 2) {
        std::cerr << "Usage: program <infile>\n";
        return -1;
    }

    std::ifstream infile(argv[1]); // This is used to open a file 
    if (!infile.is_open()) return -1; //check whether it is opened or not 

    std::map<std::string, int> wordCount;// define a map from string to int 
    std::string word;
    while (infile >> word)//read a word from the file 
    {
  		word.erase(remove_if(word.begin(), word.end(), not1(std::ptr_fun (::isalpha))), word.end()); 
      	std::cout << word  << std::endl;// display the word 
    	++wordCount[word];//add count of the word 
    }
    for (std::map<std::string, int>::iterator it = wordCount.begin(); it != wordCount.end(); ++it)
     {
           std::cout << it->first <<" : "<< it->second << std::endl;//display the frequency, we can write the output to a file 
     }
    return 0;
}
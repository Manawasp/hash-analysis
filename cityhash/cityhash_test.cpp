#include <iostream>
#include <fstream>
#include <cstring>
#include <cstdlib>
#include <cmath>
#include <city.h> // std::CityHash128
#include <algorithm> // std::sort
#include <vector> // std::vector

// Read file and generate hash for each line
std::vector<uint64>* hash_from_file(std::fstream *file,
                                    const uint64 constraint,
                                    uint64 maxCount) {
  std::vector<uint64>* v = new std::vector<uint64>();
  std::string str;
  uint64 count = 0;

  while (std::getline(*file, str))
  {
    if (maxCount != 0 && count >= maxCount) {
      break;
    }
    uint64 h = CityHash64(str.c_str(), str.size());
    if (constraint != 0) {
      h %= constraint;
    }
    v->push_back(h);
    count++;
  }
  return v;
}

// Iter to match duplication
uint64 find_duplication(std::vector<uint64> *v) {
  uint32 duplicat = 0;
  for (std::vector<uint64>::iterator it=v->begin(); it != v->end() && it != v->end() - 1; ++it)
  {
    std::vector<uint64>::iterator next = it + 1;
    if (*it == *next) {
      duplicat++;
    }
  }
  return duplicat;
}

void printResult(std::vector<uint64> *v, uint64 duplicat) {
  std::cout << "Hash: " << v->size() << "   ||   Duplicate: " << duplicat;
  if (v->size() > 0) {
    std::cout << "  ||   " << duplicat * 100 / v->size() << "%";
  }
  std::cout << std::endl;
}

void cityhash_test(std::string filename, uint64 constraint) {
  // Open file
  std::fstream file;
  file.open(filename.c_str(), std::fstream::in);
  if (!file)
  {
    std::cout << "Error: file not found" << std::endl;
    return;
  }
  std::vector<uint64>* v = hash_from_file(&file, constraint, 20);
  file.close();

  std::sort(v->begin(), v->end());
  uint64 duplicat = find_duplication(v);
  printResult(v, duplicat);
}

int main(int argc, char** argv)
{
  if (argc < 2) {
    std::cout << "./cityhash_text [FILENAME]" << std::endl;
    return -1;
  }
  uint64 constraint = std::pow(62, 6);
  cityhash_test(argv[1], constraint);
  return 0;
}

#include <iostream>
using namespace std;

main()
{
  int * bad_pointer;
  int x = 9;
  *bad_pointer = x;
  return 0;
}

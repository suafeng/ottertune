#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

//using namespace std;

int main()
{
        int sizeG = 17;
        size_t gb_in_bytes = 1 << 30; // 1 GB in bytes (2^30).
        printf("start malloc \n");


        char x = 'a';
        for (int k = 0; k < sizeG;k++)
        {
                char *ptr = (char *) malloc(gb_in_bytes);
                for (int i = 0; i < gb_in_bytes; i++)
                        ptr[i] = x;

                if(ptr == NULL)
                {
                        printf("Error! memory not allocated.");
                        exit(0);
                }

        }
        printf("end malloc \n");
        printf("size %dG \n", sizeG);
 while(1)
        {
            sleep(1);
        }


}
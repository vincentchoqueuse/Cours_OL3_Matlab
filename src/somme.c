#include <stdio.h>

int main( void )
{
    long int k,S=0;
    for (k=0;k<10000000;k++)
    {
        S=S+k;
    }
    printf ("%li\n" ,S);
    return 0;
}
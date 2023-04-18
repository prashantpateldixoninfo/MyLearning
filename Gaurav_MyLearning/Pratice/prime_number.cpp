#include<iostream>
using namespace std;
int main()
{
    int number, p=0;
    cout << "\n Enter the number upto which you want to see prime number=";
    cin >> number;
    for (int i =2 ; i<= number ; i++)
    {  
        p=0;
        for(int j=2 ; j < i ; j++)
        {
            if ( i % j == 0)
            {

                p= 1;
            }
        }
        if ( p == 0)
        {
            cout << "\n" << i << " is a prime number\n ";
        }
    }
    return 0;
}



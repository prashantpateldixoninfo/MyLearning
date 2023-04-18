#include<iostream>
using namespace std;
int main()
{
    int num , sum = 0;
    cout << "\n Enter the number upto which you want to print sum of all even number";
    cin >> num;
    for( int j=2 ; j<= num ; j= j+2)
    {
        sum = sum + j ;
    }
    cout << "\n Sum of all even number ="<<sum<<"\n";

    return 0;
}


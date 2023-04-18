#include<iostream>
using namespace std;
 
int main()
{
    int num1 = 0, num2 = 1, num3=0, last;
    cout<<"\nEnter the number upto which you want to see fibronacci series=";
    cin>> last;
    cout<<"\n fibronacci series="<< num1 <<"\t"<<num2<< "\t";
    while( num3 <= last )
    {
        num3 = num1 + num2;
        if( num3<= last)
        {
        cout << num3 << "\t";
        num1 = num2;
        num2 = num3;
        }
    }
    cout<<"\n";
    return 0;
}


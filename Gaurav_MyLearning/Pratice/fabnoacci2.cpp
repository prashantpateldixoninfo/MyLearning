#include<iostream>
using namespace std;

int main()
{
    int num1 = 0, num2 = 1, num3=0, last;
    cout<<"\nEnter the number upto which you want to check in fabronacci series=";
    cin>> last;
    while( num3 < last )
    {
        num3 = num1 + num2;
 
        
        num1 = num2;
        num2 = num3;
        
    }
    if(num3 == last)
    {
        cout<<"\n number enterd was the part of fabronacci series\n";
    }
    else 
    {
        cout << "\n number entered was not the part of fabronacci series\n";
    }
    return 0;
}


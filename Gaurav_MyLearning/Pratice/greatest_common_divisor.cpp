#include<iostream>
using namespace std;

int main()
{
    int num1 , num2 , divisor = 5 , temp;
    cout << "\nEnter the First number=" ;
    cin >> num1 ;
    cout << "\nEnter the Second number=" ;
    cin >> num2 ;
    if ( num1 == num2 )
    {
        divisor = num1 ;
    }
    else if ( num1%num2 == 0 )
    {
        divisor = num2 ;
    }
    else if ( num2%num1 == 0 )
    {
        divisor =  num1 ;
    }
    else if ( num1 > num2 )
    {
        temp = num2/2;

        for( int i = temp ; i >= 1 ; i--)
        {
            if( (num1%i) == 0 && (num2%i)== 0 )
            { 
                divisor = i ;
                break;
            }
        }
    }
    else if ( num2 > num1 )
    {
        temp = num1/2;

        for( int i = temp ; i >= 1 ; i--)
        {
            if( (num1%i) == 0 && (num2%i)== 0 )
            { 
                divisor = i ;
                break;
            }
        }
    }
    else
    {
        cout<<"\n Program not executed successfully\n ";
    }

    cout<<"\n Greatest Common divisor number=="<< divisor <<"\n" ;
    return 0;
}
 

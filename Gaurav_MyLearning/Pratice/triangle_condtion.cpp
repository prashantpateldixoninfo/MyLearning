#include <iostream>

using namespace std;

int main()
{   int side1, side2, side3;
    cout << "Gaurav Pandey" ;
    cout << "\n Enter the first side of triangle==";
    cin >> side1;
    cout << "\n Enter the second side of triangle==";
    cin >> side2;
    cout << "\n Enter the third side of triangle==";
    cin >> side3;
    if ( side1 == side2 && side2 == side3 )
    {
        cout << "\nTriangle is equilateral triangle\n ";
    }
    else if ( side1 == side2 || side2 == side3 || side3 == side1 )
    {
        cout << " \n Trianle is isoceles triangle \n";
    }
 
    else
    {
        cout<<"\n triangle is scaler triangle\n ";
    }

    return 0;
}

#include <iostream>
using namespace std;

int main() {
    int age, marks;

    cout << "Enter age: ";
    cin >> age;

    cout << "Enter marks: ";
    cin >> marks;

    // Decision Path 1
    if (age < 18) {
        cout << "Minor student" << endl;
    }

    // Decision Path 2
    if (age >= 18 && marks >= 90) {
        cout << "Eligible for Scholarship" << endl;
    }

    // Decision Path 3
    else if (age >= 18 && marks >= 50) {
        cout << "Eligible for Admission" << endl;
    }

    // Decision Path 4
    else {
        cout << "Not Eligible" << endl;
    }

    return 0;
}

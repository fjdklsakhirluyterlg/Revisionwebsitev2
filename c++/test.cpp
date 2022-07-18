#include <iostream>
#include <string>
#include <cstdlib>
#include <ctime>
#include <cmath>
using namespace std;

float generateπ_from_random(int n){
    int ins = 0;
    int outs = 0;
    for(int i = 0; i < n; i++){
        srand((unsigned) time(0));
        int x = rand() % 2;
        int y = rand() % 2;
        float distance = pow(x, 2) + pow(x, 2);
        if (distance <= 1){
            ins = ins + 1;
        } else {
            outs = outs + 1;
        }
    }

    return 4*ins/outs;
}

int main(){
    return 0;
}
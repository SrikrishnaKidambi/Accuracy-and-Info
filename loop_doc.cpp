#include<iostream>

int findSum(int arr[],int n){
    int sum=0;
    for(int i=0;i<n;i++){
        sum+=arr[i];
    }
    return sum;
}
int main(){
    int n;
    cin>>n;
    int arr[n];
    for(int i=0;i<n;i++){
        arr[i]=i;
    }
    int sum=findSum(arr,n);
    cout<<"The sum of the array is: "<<sum<<endl;
    return 0;
}
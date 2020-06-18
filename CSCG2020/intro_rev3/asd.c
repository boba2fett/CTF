#include<stdio.h>
#include<stdlib.h>

int main(int argc,char *argv[])
{
   int16_t s1[28]={108, 112, 96, 55, 97, 60, 113, 76, 119, 30, 107, 72, 111, 112, 116, 40, 102, 45, 102, 42, 44, 111, 125, 86, 15, 21, 74,0};
   for(int i=0;i<27;i++)
   {
        s1[i]+=2;
        s1[i]=s1[i]^i+10U;
   }
   char s[28];
   for(int i=0;i<28;i++)
   {
        s[i]=s1[i];
   }
   printf("%s\n",(char*)s);
   printf("%x\n",s[25]);
   printf("%x\n",s[26]);
   printf("%x\n",s[27]);
}

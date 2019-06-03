#include"uart.h"
#include"delay.h"
void UART_Init(unsigned char TH){
	TMOD=0x22; // timer 1 in mode 2 (8-bit auto-reload) to set baud rate
	TH1=TH;
	SCON=0x50;
	TR1=1;
}
void UART_TxChar(char ch){
	SBUF=ch;
	while(TI==0);
	TI=0;
}
//char UART_RxChar(){
//	while(RI==0);
//	RI=0;
//	return SBUF;
//}
void UART_TxString(char* str){
	while(*str){
		ms_Delay(1);
		UART_TxChar(*str++);
	}
}

//unsigned char UART_RxString(char *ptr_string)
//{
//    char ch;
//    unsigned char len = 0;
//    while(1)
//    {
//        ch=UART_RxChar();    //Receive a char
//        UART_TxChar(ch);     //Echo back the received char

//        if((ch=='\r') || (ch=='\n')) //read till enter key is pressed
//        {                             //once enter key is pressed null terminate the string
//            ptr_string[len]=0;           //and break the loop
//            break;                  
//        }
//        else if((ch=='\b') && (len!=0))
//        {
//            len--;    //If backspace is pressed then decrement the index to remove the old char
//        }
//        else
//        {
//            ptr_string[len]=ch; //copy the char into string and increment the index
//            len++;
//        }
//    }
//  return len;   
//}
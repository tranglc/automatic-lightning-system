#include <stdio.h>
#include "lcd.h"
#include"i2c1.h"
#include "i2c.h"
#include "uart.h"
#include "delay.h"
#include "BH-1750.h"

unsigned long lux_value = 0;
char str[6];
unsigned char flag=0;
unsigned char duty_cycle=0;

void LED_Handler(char);
void Update_Lux();
void BLE() interrupt 4{
	if(TI==1){
		TI=0;
		return;
	}else{
		IE=0;
		if(SBUF==101){
			Update_Lux();
		}else if(97<=SBUF&&SBUF<=100){
			LED_Handler(SBUF);
		}
		RI=0;
		IE=0x90;
		return;
	}
}
void Update_Lux(){
			lux_value = get_lux_value(cont_L_res_mode,20);
			sprintf(str,"%06lu",lux_value);
			LCD_CMDWrite(0x87);
			LCD_DisplayString(str);
			sprintf(str,"%06lu\r\n",lux_value);
			UART_TxString(str);
			return;
}
void LED_Handler(unsigned char mode){
	if(mode==97){
		duty_cycle=0;
	}else if(mode==98){
		duty_cycle=255;
	}
	else if(mode==99){
		if(duty_cycle==255)
			return;
		duty_cycle++;
	}else if(mode==100){
		if(duty_cycle==0)
			return;
		duty_cycle--;
	}
	I2C_Start1();
	I2C_Write1(0xFE);
	I2C_Write1(duty_cycle);
	I2C_Stop1();
	sprintf(str,"%03d",(int)duty_cycle);
	LCD_CMDWrite(0xCB);
	LCD_DisplayString(str);
	return;
}

void main(){
	unsigned char i=0;
	UART_Init(0xFD);
	LCD_Init();
	I2C_Init();
	I2C_Init1();
	BH1750_init();
	LCD_CMDWrite(0x80);
	LCD_DisplayString("Lux:");
	LCD_CMDWrite(0xC0);
	LCD_DisplayString("LED POWER:");
	IE=0x90;
		while(1){
		}
	}
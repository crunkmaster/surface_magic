#include <Servo.h>
Servo Q1, Q2, Q3, Q4 ;
int q1 = A0 ;
int q2 = A3 ;
int q3 = A1 ;
int q4 = A2 ;
//includes servos and gives them variables accordingly

//creates variables for positions
int Z1, Z2, Z3, Z4 ;
int z1, z2, z3, z4 ;

//variables for position
int x_r, y_r;
int x, y;

//constants
double K_x =.25;
double K_y =.25;
int L=290;
int l=290;
double width ;
double height ;

//threshold
int mu = 10;

void setup(){
    Serial.begin(9600);

    //attatching all of the servos
    Q1.attach( 3 ) ;
    Q2.attach( 11 ) ;
    Q3.attach( 9 ) ;
    Q4.attach( 10 ) ;
    //setting all of the positions equal to 50
    Q1.writeMicroseconds( 1500 ) ;
    Q2.writeMicroseconds( 1500 ) ;
    Q3.writeMicroseconds( 1500 ) ;
    Q4.writeMicroseconds( 1500 ) ;
    delay(15) ;
    get_sizes( &width, &height );
    Serial.print( width );
    Serial.print( height );
}

void loop(){
    //get ball coordinates and distance from line
    char buffer[30] ;
    get_coordinates( &x_r, &y_r, &x, &y );
    sprintf(buffer, "%d %d %d %d\n", x_r, y_r, x, y);
    Serial.print( buffer );

    if ( x_r == 1000 ) {
        Serial.print( "ball out of range\n" );
        reset();
    }

    //reference in quadrant 1
    if( y_r <= L/2 && x_r <= l/2 ){
        Z1=50 - ( y_r )/( L - y_r )*(K_y * (y-y_r)) - (x_r) / (l - x_r)* ( K_x * (x-x_r));
        Z2= 50 -( y_r ) / ( L - y_r )* (K_y * (y-y_r)) + ( K_x * (x-x_r));
        Z3= 50 + (K_y * (y-y_r)) - ( x_r )/( l - x_r) * ( K_x * (x-x_r));
        Z4= -Z1 + Z2 + Z3 ;
        Serial.print("quadrant 1\n");
    }

    //quadrant 2
    if (y_r <= L/2 && x_r > l/2){
        Z1= 50 - ( y_r ) / ( L -y_r ) * (K_y * (y-y_r)) + (-K_x * (x-x_r));
        Z2= 50 -( y_r ) /( L - y_r ) * (K_y * (y-y_r)) - ((l - x_r)/ x_r) * (-K_x * (x-x_r));
        Z3= 50 + (K_y * (y-y_r))+ ( -K_x * (x-x_r));
        Z4=-Z1+Z2+Z3;
        Serial.print("quadrant 2\n");
    }
    //quadrant 3
    if ( y_r > L/2 && x_r<l/2){
        Z1= 50 +(-K_y * (y-y_r)) - ((x_r)/(l-x_r)) * ( K_x * (x-x_r));
        Z2= 50 + (-K_y * (y-y_r)) + ( K_x * (x-x_r));
        Z3= 50 - ((L-y_r)/y_r)*(-K_y * (y-y_r)) - (x_r/(l-x_r))*( K_x * (x-x_r));
        Z4=-Z1+Z2+Z3;
        Serial.print("quadrant 3\n");
    }

    //quadrant 4
    if (y_r >L/2 && x_r > l/2){

        Z1=50+(-K_y*(y-y_r))+(-K_x*(x-x_r));
        Z2=50+(-K_y*(y-y_r))+((l-x_r)/x_r)*(-K_x*(x-x_r));
        Z3=50-((L-y_r)/y_r)*(-K_y*(y-y_r))+(-K_x*(x-x_r));
        Z4=-Z1+Z2+Z3;
        Serial.print("quadrant 4\n");
    }

    Q1.writeMicroseconds(Z1*10+1000);
    Q2.writeMicroseconds(Z2*10+1000);
    Q3.writeMicroseconds(Z3*10+1000);
    Q4.writeMicroseconds(Z4*10+1000);

    //treshold
    if ( y_r + mu > y && x_r + mu > x) {
        Q1.writeMicroseconds(1500);
        Q2.writeMicroseconds(1500);
        Q3.writeMicroseconds(1500);
        Q4.writeMicroseconds(1500);
    }

    z1=map(analogRead(q1),13,668,100,0);
    z2=map(analogRead(q2),12,672,100,0);
    z3=map(analogRead(q3),15,671,100,0);
    z4=map(analogRead(q4),10,668,100,0);

}

void get_coordinates(int *x_r, int *y_r, int *x, int *y){
    //checks avalible serial packets
    if (Serial.available()>0)

        if (Serial.findUntil("-","-")){
            *x_r= Serial.parseInt();
            *y_r= Serial.parseInt();
            *x = Serial.parseInt();
            *y = Serial.parseInt();
        }
}

void get_sizes(double *width, double *height) {
    while ( 1 ) {
        if (Serial.available() <= 0 ) {
            delay( 100 ) ;
        }
        if (Serial.available() > 0) {
           if (Serial.findUntil("*", "*")) {
                *width = Serial.parseInt();
                *height = Serial.parseInt();
            }
            break;
        }
    }
}

void reset() {
    Q1.writeMicroseconds( 1500 ) ;
    Q2.writeMicroseconds( 1500 ) ;
    Q3.writeMicroseconds( 1500 ) ;
    Q4.writeMicroseconds( 1500 ) ;
    delay(5000) ;
}

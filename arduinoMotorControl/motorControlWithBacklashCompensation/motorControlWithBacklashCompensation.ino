
#include <AccelStepper.h>

AccelStepper down (1, 2, 1);
AccelStepper front (1, 4, 3);
AccelStepper right (1, 6, 5);
AccelStepper back (1, 8, 7);
AccelStepper left (1, 10, 9);
AccelStepper up (1, 12, 11);


#define MOTOR_MAX_SPEED 100000
#define MOTOR_MAX_ACC 100000

#define TURN_QUARTER 200
#define TURN_HALF 400

const int enable_d = 16;
const int enable_f = 17;
const int enable_r = 18;
const int enable_b = 19;
const int enable_l = 20;
const int enable_u = 21;

enum lastMove {
    TURN_DIR_CW = 0,
    TURN_DIR_ACW,
    TURN_DIR_NONE,
};

lastMove uLast = TURN_DIR_NONE;
lastMove fLast = TURN_DIR_NONE;
lastMove lLast = TURN_DIR_NONE;
lastMove rLast = TURN_DIR_NONE;
lastMove dLast = TURN_DIR_NONE;
lastMove bLast = TURN_DIR_NONE;

void setup()
{
  //Declaring motor enable pins
  pinMode (enable_d, OUTPUT);
  pinMode (enable_f, OUTPUT);
  pinMode (enable_r, OUTPUT);
  pinMode (enable_b, OUTPUT);
  pinMode (enable_l, OUTPUT);
  pinMode (enable_u, OUTPUT);

  digitalWrite (enable_d, HIGH);
  digitalWrite (enable_f, HIGH);
  digitalWrite (enable_r, HIGH);
  digitalWrite (enable_b, HIGH);
  digitalWrite (enable_l, HIGH);
  digitalWrite (enable_u, HIGH);

  // Setting speed, acceleration of motors
  down.setMaxSpeed(MOTOR_MAX_SPEED);
  down.setAcceleration(MOTOR_MAX_ACC);

  front.setMaxSpeed(MOTOR_MAX_SPEED);
  front.setAcceleration(MOTOR_MAX_ACC);

  right.setMaxSpeed(MOTOR_MAX_SPEED);
  right.setAcceleration(MOTOR_MAX_ACC);

  back.setMaxSpeed(MOTOR_MAX_SPEED);
  back.setAcceleration(MOTOR_MAX_ACC);

  left.setMaxSpeed(MOTOR_MAX_SPEED);
  left.setAcceleration(MOTOR_MAX_ACC);

  up.setMaxSpeed(MOTOR_MAX_SPEED);
  up.setAcceleration(MOTOR_MAX_ACC);

    //Initialise serial and wait for port to open:
  Serial.begin(9600);

  while (!Serial) {
    ; // wait for serial port to connect.
  }
}

void loop()
{
  char readin;
  char side;
  char dir;
  bool sendAck = false;

  int backlashOffset = 10;
  int rotation = 0;


  while (Serial.available() > 0) {
    side = 0;
    dir = 0;
    sendAck = true;
    readin = Serial.read();


    if (readin == 'D' || readin == 'F' || readin == 'R' || readin == 'B' || readin == 'L' || readin == 'U') {
      side = readin;
      readin = Serial.read();
      if (readin == '\'' || readin == '2') {
        dir = readin;
      }
    }

    if (side == 'D') {
      digitalWrite (enable_d, LOW);
      if (dir == '\'') {
        rotation = TURN_QUARTER + ((dLast != TURN_DIR_ACW) ? backlashOffset : 0);
        down.moveTo(rotation + down.currentPosition());
        dLast = TURN_DIR_ACW;
        while (down.distanceToGo() != 0) {
          down.run();
        }
      }
      else if (dir == '2') {
        rotation = TURN_HALF + ((dLast != TURN_DIR_ACW) ? backlashOffset : 0);
        down.moveTo(rotation + down.currentPosition());
        dLast = TURN_DIR_ACW;
        while (down.distanceToGo() != 0) {
          down.run();
        }
      }
      else {
        rotation = TURN_QUARTER + ((dLast != TURN_DIR_CW) ? backlashOffset : 0);
        down.moveTo(down.currentPosition() - rotation);
        dLast = TURN_DIR_CW;
        while (down.distanceToGo() != 0) {
          down.run();
        }
      }
      digitalWrite (enable_d, HIGH);
    }

    else if (side == 'F') {
      digitalWrite (enable_f, LOW);
      if (dir == '\'') {
        rotation = TURN_QUARTER + ((fLast != TURN_DIR_ACW) ? backlashOffset : 0);
        front.moveTo(rotation + front.currentPosition());
        fLast = TURN_DIR_ACW;
        while (front.distanceToGo() != 0) {
          front.run();
        }
      }
      else if (dir == '2') {
        rotation = TURN_HALF + ((fLast != TURN_DIR_ACW) ? backlashOffset : 0);
        front.moveTo(rotation + front.currentPosition());
        fLast = TURN_DIR_ACW;
        while (front.distanceToGo() != 0) {
          front.run();
        }
      }
      else {
        rotation = TURN_QUARTER + ((fLast != TURN_DIR_CW) ? backlashOffset : 0);
        front.moveTo(front.currentPosition() - rotation);
        fLast = TURN_DIR_CW;
        while (front.distanceToGo() != 0) {
          front.run();
        }
      }
      digitalWrite (enable_f, HIGH);
    }

    else if (side == 'R') {
      digitalWrite (enable_r, LOW);
      if (dir == '\'') {
        rotation = TURN_QUARTER + ((rLast != TURN_DIR_ACW) ? backlashOffset : 0);
        right.moveTo(rotation + right.currentPosition());
        rLast = TURN_DIR_ACW;
        while (right.distanceToGo() != 0) {
          right.run();
        }
      }
      else if (dir == '2') {
        rotation = TURN_HALF + ((rLast != TURN_DIR_ACW) ? backlashOffset : 0);
        right.moveTo(rotation + right.currentPosition());
        rLast = TURN_DIR_ACW;
        while (right.distanceToGo() != 0) {
          right.run();
        }
      }
      else {
        rotation = TURN_QUARTER + ((rLast != TURN_DIR_CW) ? backlashOffset : 0);
        right.moveTo(right.currentPosition() - rotation);
        rLast = TURN_DIR_CW;
        while (right.distanceToGo() != 0) {
          right.run();
        }
      }
      digitalWrite (enable_r, HIGH);
    }

    else if (side == 'B') {
      digitalWrite (enable_b, LOW);
      if (dir == '\'') {
        rotation = TURN_QUARTER + ((bLast != TURN_DIR_ACW) ? backlashOffset : 0);
        back.moveTo(rotation + back.currentPosition());
        bLast = TURN_DIR_ACW;
        while (back.distanceToGo() != 0) {
          back.run();
        }
      }
      else if (dir == '2') {
        rotation = TURN_HALF + ((bLast != TURN_DIR_ACW) ? backlashOffset : 0);
        back.moveTo(rotation + back.currentPosition());
        bLast = TURN_DIR_ACW;
        while (back.distanceToGo() != 0) {
          back.run();
        }
      }
      else {
        rotation = TURN_QUARTER + ((bLast != TURN_DIR_CW) ? backlashOffset : 0);
        back.moveTo(back.currentPosition() - rotation);
        bLast = TURN_DIR_CW;
        while (back.distanceToGo() != 0) {
          back.run();
        }
      }
      digitalWrite (enable_b, HIGH);
    }

    else if (side == 'L') {
      digitalWrite (enable_l, LOW);
      if (dir == '\'') {
        rotation = TURN_QUARTER + ((lLast != TURN_DIR_ACW) ? backlashOffset : 0);
        left.moveTo(rotation + left.currentPosition());
        lLast = TURN_DIR_ACW;
        while (left.distanceToGo() != 0) {
          left.run();
        }
      }
      else if (dir == '2') {
        rotation = TURN_HALF + ((lLast != TURN_DIR_ACW) ? backlashOffset : 0);
        left.moveTo(rotation + left.currentPosition());
        lLast = TURN_DIR_ACW;
        while (left.distanceToGo() != 0) {
          left.run();
        }
      }
      else {
        rotation = TURN_QUARTER + ((lLast != TURN_DIR_CW) ? backlashOffset : 0);
        left.moveTo(left.currentPosition() - rotation);
        lLast = TURN_DIR_CW;
        while (left.distanceToGo() != 0) {
          left.run();
        }
      }
      digitalWrite (enable_l, HIGH);
    }

    else if (side == 'U') {
      digitalWrite (enable_u, LOW);
      if (dir == '\'') {
        rotation = TURN_QUARTER + ((uLast != TURN_DIR_ACW) ? backlashOffset : 0);
        up.moveTo(rotation + up.currentPosition());
        uLast = TURN_DIR_ACW;
        while (up.distanceToGo() != 0) {
          up.run();
        }
      }
      else if (dir == '2') {
        rotation = TURN_HALF + ((uLast != TURN_DIR_ACW) ? backlashOffset : 0);
        up.moveTo(rotation + up.currentPosition());
        uLast = TURN_DIR_ACW;
        while (up.distanceToGo() != 0) {
          up.run();
        }
      }
      else {
        rotation = TURN_QUARTER + ((uLast != TURN_DIR_CW) ? backlashOffset : 0);
        up.moveTo(up.currentPosition() - rotation);
        uLast = TURN_DIR_CW;
        while (up.distanceToGo() != 0) {
          up.run();
        }
      }
      digitalWrite (enable_u, HIGH);
    }

  }
  if (sendAck == true)
  {
    Serial.write("ack\n");
    sendAck = false;
  }

}

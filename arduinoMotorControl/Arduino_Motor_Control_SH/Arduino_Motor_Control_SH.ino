
#include <AccelStepper.h>

AccelStepper down (1, 2, 1);
AccelStepper front (1, 4, 3);
AccelStepper right (1, 6, 5);
AccelStepper back (1, 8, 7);
AccelStepper left (1, 10, 9);
AccelStepper up (1, 12, 11);


#define MOTOR_MAX_SPEED 10000
#define MOTOR_MAX_ACC 20000

const int enable_d = 16;
const int enable_f = 17;
const int enable_r = 18;
const int enable_b = 19;
const int enable_l = 20;
const int enable_u = 21;

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

  readin = Serial.read();

  while (Serial.available() > 0) {

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
        down.moveTo(203 + down.currentPosition());
        while (down.distanceToGo() != 0) {
          down.run();
        }
      }
      else if (dir == '2') {
        down.moveTo(403 + down.currentPosition());
        while (down.distanceToGo() != 0) {
          down.run();
        }
      }
      else {
        down.moveTo(down.currentPosition() - 203);
        while (down.distanceToGo() != 0) {
          down.run();
        }
      }
      digitalWrite (enable_d, HIGH);
    }

    else if (side == 'F') {
      digitalWrite (enable_f, LOW);
      if (dir == '\'') {
        front.moveTo(203 + front.currentPosition());
        while (front.distanceToGo() != 0) {
          front.run();
        }
      }
      else if (dir == '2') {
        front.moveTo(403 + front.currentPosition());
        while (front.distanceToGo() != 0) {
          front.run();
        }
      }
      else {
        front.moveTo(front.currentPosition() - 203);
        while (front.distanceToGo() != 0) {
          front.run();
        }
      }
      digitalWrite (enable_f, HIGH);
    }

    else if (side == 'R') {
      digitalWrite (enable_r, LOW);
      if (dir == '\'') {
        right.moveTo(203 + right.currentPosition());
        while (right.distanceToGo() != 0) {
          right.run();
        }
      }
      else if (dir == '2') {
        right.moveTo(403 + right.currentPosition());
        while (right.distanceToGo() != 0) {
          right.run();
        }
      }
      else {
        right.moveTo(right.currentPosition() - 203);
        while (right.distanceToGo() != 0) {
          right.run();
        }
      }
      digitalWrite (enable_r, HIGH);
    }

    else if (side == 'B') {
      digitalWrite (enable_b, LOW);
      if (dir == '\'') {
        back.moveTo(203 + back.currentPosition());
        while (back.distanceToGo() != 0) {
          back.run();
        }
      }
      else if (dir == '2') {
        back.moveTo(403 + back.currentPosition());
        while (back.distanceToGo() != 0) {
          back.run();
        }
      }
      else {
        back.moveTo(back.currentPosition() - 203);
        while (back.distanceToGo() != 0) {
          back.run();
        }
      }
      digitalWrite (enable_b, HIGH);
    }

    else if (side == 'L') {
      digitalWrite (enable_l, LOW);
      if (dir == '\'') {
        left.moveTo(203 + left.currentPosition());
        while (left.distanceToGo() != 0) {
          left.run();
        }
      }
      else if (dir == '2') {
        left.moveTo(403 + left.currentPosition());
        while (left.distanceToGo() != 0) {
          left.run();
        }
      }
      else {
        left.moveTo(left.currentPosition() - 203);
        while (left.distanceToGo() != 0) {
          left.run();
        }
      }
      digitalWrite (enable_l, HIGH);
    }

    else if (side == 'U') {
      digitalWrite (enable_u, LOW);
      if (dir == '\'') {
        up.moveTo(203 + up.currentPosition());
        while (up.distanceToGo() != 0) {
          up.run();
        }
      }
      else if (dir == '2') {
        up.moveTo(403 + up.currentPosition());
        while (up.distanceToGo() != 0) {
          up.run();
        }
      }
      else {
        up.moveTo(up.currentPosition() - 203);
        while (up.distanceToGo() != 0) {
          up.run();
        }
      }
      digitalWrite (enable_u, HIGH);
    }

    side = 0;
    dir = 0;
    readin = Serial.read();

  }

}

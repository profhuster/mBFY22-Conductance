/*
 * Half_Breadboard_Rnd_22a
 * ProfHuster@gmail.com
 * 2021-02014
 *
 * This is case that holds a half breadboard
 * 
 * v21a - Initial build
 * v21b - Add lid
 * v21c - Parameterized snaps in lid
 *        Breadboard is "upsidedown"
 * v22a - Making 1/2 breadboard project box
 *        Added blocks to position BB
 */
include <screws.scad>
include <RoundedBottomBox_21f.scad>

eps = 0.1;
eps2 = 2 * eps;
$fn=24;

echo("\n==== S2Mini_Stepper_Case ====\n");

printBase = false;
flipLid = true;
printLid = true;
printHBB = false;
// RPiRndLid();
// BREADBOARD PARAMETERS
// Half Breadboard
boardL = 83;
boardW = 56;
boardH = 9.5;

// Model tabs as square of 2x2x6 mm
tabL = 2;
tabH = 6;
// Positions of tabs on BB
tabX = [56, 56, 4, 50]; 
tabY = [14, 68, 83, 83];

// CASE PARAMETERS
caseTh = 2.5;
caseR = 3;
caseAngle = 30;
caseClrX = 3; // clearance around board for snaps
electClr = 10; // Height of electronics above bb

caseX = boardW + tabL + 2*caseClrX + 2*caseTh;
caseY = boardL + tabL + 1*caseClrX + 2*caseTh; // snap only in back
caseZ = boardH + caseTh;
lidZ = 18;

// Blocks to position breadboad
lBl = 10;
hBl = 2;
wBl = [4,4,4,4,3.0];
xBl = [caseTh, caseTh, caseX-caseTh-wBl[2], caseX-caseTh-wBl[3], 
        (caseX-caseTh-wBl[4])/2];
yBl = [caseTh, 86-lBl, caseTh, 86-lBl, 86];
zBl = caseTh;
thBl = [0, 0, 0, 0, 90];

// Lid Stuff
// Snap parameters
// Stick up tabs with snap ridges
// X,Y,L,lidZ,R,TH,Angle
srX0 = [0, 0, caseX, caseX];
srY0 = [20+caseTh+0.5, caseY-caseTh-0.5, 
           caseTh+0.5, caseY-caseTh-20-0.5];
srL0 = [20, 20, 20, 20];
srAngX0 = [0, 0, 0, 0];
srAngY0 = [180, 180, 180, 180];
srAngZ0 = [180, 180, 0, 0];
srParams0 = [srX0, srY0, srL0, srAngX0, srAngY0, srAngZ0];

// Lid Vents
hV1=10;
hV2=10;
RPventLX = [21, caseX+eps]; // Clearance for S2Mini, hole for wires
RPventLY = [0, 55];
RPventLZ = [lidZ-hV1+eps,lidZ-hV2+eps];
RPventLW = [27, 10];
RPventLH = [hV1,hV2];
RPventLL = [2*caseTh,2*caseTh];
RPventLAng = [0,90];


// Bottom
module BBRndCase(){
  union(){
    difference(){
      color("lightblue")
      RoundedBottom(caseX,caseY,caseZ,caseR,
        caseTh,caseAngle);
    }
    // Add positioning block for BB
    for(i=[0:len(xBl)-1]){
        color("lavender")
            translate([xBl[i],yBl[i],zBl])
            rotate([0,0,thBl[i]])
            cube([wBl[i],lBl,hBl]);
        
    }
  }
}

module RPiRndLid(){
  union(){
    difference(){
      color("wheat") 
      RoundedLid(caseX,caseY,lidZ,caseR,
          caseTh,caseAngle, srParams0);
      // Access holes (I call "vents")
      for(i = [0:len(RPventLX)-1]){
        translate([RPventLX[i],
          RPventLY[i]-eps, 
          RPventLZ[i]])
          rotate([0,0,RPventLAng[i]])
          color("yellow")
          cube([RPventLW[i],RPventLL[i],RPventLH[i]]);
      }
    }
  }
}



if(printBase){
  BBRndCase();
}

if(printHBB){
    translate([caseTh+caseClrX,caseTh+0.5,caseTh])
        halfBB();
}

if(printLid){
  if(flipLid){
    translate([-caseX-5,0,0])
      RPiRndLid();
  } else {
    translate([caseX,0,caseZ+lidZ+4])
      rotate([0,180,0])
      RPiRndLid();
  }
}

module halfBB(){
    color("pink"){
        cube([boardW, boardL,, boardH]);
        for(i = [0:len(tabX)-1]){
            echo(i);
            translate([tabX[i], tabY[i], 0])
                cube([tabL, tabL, tabH]);
        }
    }
}

// EOF
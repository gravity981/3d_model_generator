//token
token_diameter=27.3;
token_height=2;

//key ring hole
hole_diameter=4;
distance=3; //distance from border

//decal
decal_enabled=true;
character="♣";
size=38;
y_offset=-4;
z_rotation=0;
font="Helvetica:style=Bold";

difference() {
    cylinder(token_height, token_diameter, token_diameter);
    
    if(decal_enabled) {
        #rotate([0,0,z_rotation]) {
            translate([0,y_offset,-1]) {
                linear_extrude(height=token_height+2) {
                    text(character,font=font,size=size,halign="center",valign="center",script="utf-8");
                }
            }
        }
    }
    
    #translate([0,token_diameter-hole_diameter-distance,-1]) {
        cylinder(token_height+2, hole_diameter, hole_diameter);
    }
}
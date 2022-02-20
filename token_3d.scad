//token
token_diameter=27.3;
token_height=2;

//key ring hole
hole_diameter=4;
hole_border_distance=3; //distance from border

//decal
decal_enabled=true;
decal_text="A"; //♣€★♥♦♠
z_rotation=0;
font="Stencilia\\-A:style=Regular";
manual_font_size_enabled=false;
manual_font_size=10;
font_size=manual_font_size_enabled ? manual_font_size : 0.0055*pow(token_diameter,2)+1.17*token_diameter+(-1.95);
manual_y_offset_enabled=false;
manual_y_offset=-5;
y_offset=manual_y_offset_enabled ? manual_y_offset : 0.0005*pow(token_diameter,2)+0.117*token_diameter+(-6.6);
x_offset=0;

difference() {
    cylinder(token_height, token_diameter, token_diameter);
    
    if(decal_enabled) {
        #rotate([0,0,z_rotation]) {
            translate([x_offset,y_offset,-1]) {
                linear_extrude(height=token_height+2) {
                    text(decal_text,font=font,size=font_size,halign="center",valign="center",script="utf-8");
                }
            }
        }
    }
    
    #translate([0,token_diameter-hole_diameter-hole_border_distance,-1]) {
        cylinder(token_height+2, hole_diameter, hole_diameter);
    }
}

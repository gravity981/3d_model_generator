token_diameter=27.3;
token_height=2;
token_radius=token_diameter/2;
hole_diameter=4;
hole_border_distance=2;
hole_radius=hole_diameter/2;
decal_enabled=true;
decal_text="X";
z_rotation=0;
font="Marsh Stencil";
manual_font_size_enabled=false;
manual_font_size=10;
font_size_multiplier=1.0;
font_size=font_size_multiplier*(manual_font_size_enabled ? manual_font_size : -0.01*pow(token_diameter,2)+1.246*token_diameter-11.563);
manual_y_offset_enabled=false;
manual_y_offset=-2.8;
y_offset=manual_y_offset_enabled ? manual_y_offset : 0.0*pow(token_diameter,2)+0.0*token_diameter-3.0;
x_offset=0;

difference() {
    cylinder(token_height, token_radius, token_radius, $fn=100);
    if(decal_enabled) {
        translate([x_offset,y_offset,-1]) {
            rotate([0,0,z_rotation]) {
                linear_extrude(height=token_height+2) {
                    text(decal_text,font=font,size=font_size,halign="center",valign="center",script="utf-8");
                }
            }
        }
    }
    translate([0,token_radius-hole_radius-hole_border_distance,-1]) {
        cylinder(token_height+2, hole_radius, hole_radius, $fn=100);
    }
}

$vpr = [0,0,0];
$vpt = [0,0,-10];
$vpd = 90;

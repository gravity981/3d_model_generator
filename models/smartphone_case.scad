baseModelFilePath="/meshes/case_samsung_S20_tpu v8.3mf";
font="Marsh Stencil";
decal_text="hello world";
horizontal_offset=0;
vertical_offset=0;
font_size=10;
z_rotation=0;
case_height=150.0;
case_width=72.0;

difference() {
    import(baseModelFilePath, convexity=3);
    translate([case_height/2+horizontal_offset,case_width/2+vertical_offset,-10])
    rotate([0, 0, z_rotation])
    mirror([1,0,0])
    linear_extrude(height=20)
    text(decal_text, font=font, size=font_size, valign="center", halign="center");
}
